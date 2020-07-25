import logging

from cms.models import CMSPlugin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from filer.models import File


logger = logging.getLogger(__name__)


class FilerFileLinkable(File):
    def get_absolute_url(self) -> str:
        return self.url
    
    class Meta(File.Meta):
        proxy = True


class LinkAllMixin(models.Model):
    link_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, blank=True, null=True)
    link_instance_pk = models.PositiveIntegerField(blank=True, null=True)
    link_instance = GenericForeignKey('link_type', 'link_instance_pk')
    link_url = models.CharField(max_length=1024, blank=True)
    link_label = models.CharField(
        max_length=1024,
        blank=True,
        help_text="You can leave it empty to use the default object label, eg the page name",
    )

    class Meta:
        abstract = True

    def get_link_url(self) -> str:
        if self.link_instance:
            return self.link_instance.get_absolute_url()
        elif self.link_url:
            return self.link_url
        else:
            logger.error(f"Unable to build url for LinkAll instance - {self}")
            return ''
    
    def get_link_label(self) -> str:
        if self.link_label:
            return self.link_label
        elif self.link_instance:
            return str(self.link_instance)
        elif self.link_url:
            return self.link_url
    
    def clean(self):
        if self.link_type and not self.link_instance:
            raise ValidationError("This link types requires an object to be selected.")

    def __str__(self) -> str:
        return link_str(self)


class LinkAllPluginModel(CMSPlugin, LinkAllMixin):

    def __str__(self) -> str:
        return link_str(self)


def link_str(link_obj: LinkAllMixin) -> str:
    if link_obj.link_instance:
        return f'{link_obj.link_instance._meta.verbose_name} - {link_obj.get_link_url()}'
    elif link_obj.link_label:
        return link_obj.link_label
    elif link_obj.link_url:
        return link_obj.link_url
    else:
        return ''
