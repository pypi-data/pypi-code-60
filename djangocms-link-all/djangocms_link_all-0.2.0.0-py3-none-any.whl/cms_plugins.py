from typing import List
import logging

from cms.models import Page
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from dataclasses import dataclass
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
from django.utils.translation import gettext as _

from link_all.models import LinkAllPluginModel
from link_all.settings import LINK_ALL_MODELS


logger = logging.getLogger(__name__)


@dataclass
class SelectableModelInstance:
    pk: int
    label: str
    url: str
    is_show_url_in_select: bool


@dataclass
class SelectableModel:
    content_type_pk: int
    verbose_name: str
    instances: List[SelectableModelInstance]


@plugin_pool.register_plugin
class LinkAllPlugin(CMSPluginBase):
    module = _("Generic")
    name = _("Link all")
    model = LinkAllPluginModel
    render_template = 'link_all/link_all.html'
    text_enabled = True
    change_form_template = 'link_all/admin/link_all.html'
    
    fieldsets = [
        (None, {
            'fields': [
                'link_all_field',
                'link_label',
                'link_type',
                'link_instance_pk',
                'link_url',
            ],
        })
    ]

    def get_readonly_fields(self, request: HttpRequest, obj: LinkAllPluginModel = None) -> List[str]:
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('link_all_field',)

    def link_all_field(self, obj: LinkAllPluginModel) -> str:
        return ''

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['selectable_models'] = self._get_selectable_models()
        print(extra_context['selectable_models'])
        return super().changeform_view(request, object_id, form_url, extra_context)

    def _get_selectable_models(self) -> List[SelectableModel]:
        selectable_models: List[SelectableModel] = []
        for link_all_model in LINK_ALL_MODELS:
            content_type = ContentType.objects.get(app_label=link_all_model.app_label, model=link_all_model.model_name)
            Model = apps.get_model(link_all_model.app_label, link_all_model.model_name)
            selectable_model_instances: List[SelectableModelInstance] = []
            
            instances_all = Model.objects.all()
            if Model == Page:
                instances_all = instances_all.filter(publisher_is_draft=False)
            for instance in instances_all:
                try:
                    url = instance.get_absolute_url()
                except AttributeError:
                    logger.error(f"{Model} doesn't appear to have a `get_absolute_url()` method.")
                    url = instance.url
                selectable_model_instances.append(
                    SelectableModelInstance(
                        pk=instance.pk,
                        url=url,
                        label=str(instance),
                        is_show_url_in_select=link_all_model.is_show_url_in_select,
                    )
                )
            selectable_models.append(
                SelectableModel(
                    verbose_name=Model._meta.verbose_name.title(),
                    content_type_pk=content_type.pk,
                    instances=selectable_model_instances,
                )
            )
        return selectable_models
