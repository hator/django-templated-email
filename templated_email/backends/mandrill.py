import vanilla_django
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import ugettext as _

# Make sure you have Djrill as your email backend

class TemplateBackend(vanilla_django.TemplateBackend):
    def __init__(self, *args, **kwargs):
        vanilla_django.TemplateBackend.__init__(self, *args, **kwargs)

    def send(self, template_name, from_email, recipient_list, context, cc=None,
            bcc=None, fail_silently=False, headers=None, template_prefix=None,
            template_suffix=None, template_dir=None, file_extension=None,
            **kwargs):

        msg = EmailMessage(from_email=from_email, to=recipient_list)
        msg.template_name = template_name
        msg.global_merge_vars = context
        msg.fail_silently = fail_silently

        if cc:
            msg.cc = cc
        if bcc:
            msg.bcc = bcc

        msg.use_template_subject = kwargs.get('use_template_subject', True)
        msg.use_template_from = kwargs.get('use_template_from', True)
        msg.async = kwargs.get('async', True)

        try:
            msg.send()
        except Exception as e:
            if not fail_silently:
                raise
        return msg.extra_headers.get('Message-Id', None)
