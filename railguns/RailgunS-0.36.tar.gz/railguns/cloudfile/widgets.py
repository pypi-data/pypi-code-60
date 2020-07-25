from os.path import join

from django.conf import settings
from django.forms import widgets
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlunquote_plus
from django.utils.safestring import mark_safe


class CloudFileWidget(widgets.TextInput):

    class Media:
        js = ['cloudfile/js/scripts.js']
        css = {'all': ['s3direct/css/bootstrap-progress.min.css', 's3direct/css/styles.css']}

    def __init__(self, *args, **kwargs):
        self.dest = kwargs.pop('dest', None)
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        if value:
            file_name = os.path.basename(urlunquote_plus(value))
        else:
            file_name = ''

        tpl = join('s3direct', 's3direct-widget.tpl')
        output = render_to_string(
            tpl, {
                'policy_url': reverse('upload-params', args=['aliyun']),
                'signing_url': reverse('s3direct-signing'),
                'element_id': self.build_attrs(attrs).get('id', '') if attrs else '',
                'file_name': file_name,
                'dest': self.dest,
                'file_url': value or '',
                'name': name,
                'style': self.build_attrs(attrs).get('style', '') if attrs else '',
                'csrf_cookie_name': getattr(settings, 'CSRF_COOKIE_NAME', 'csrftoken')
            })

        return mark_safe(output)
