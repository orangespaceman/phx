import logging

from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.utils import timezone

from .models import Topic

logger = logging.getLogger(__name__)

custom_topics = [
    ('general', 'General Enquiry'),
    ('misc', 'Miscellaneous / Other'),
]


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'Form-input--text'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'Form-input--text'}),
    )
    topic = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(attrs={'class': 'Form-select'}),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'Form-textarea'}),
    )

    # honeypot
    phone_no = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'u-hidden'}),
    )

    def __init__(self, *args, **kwargs):
        # add custom topics to start and end of dropdown list
        super(ContactForm, self).__init__(*args, **kwargs)
        choices = [(topic.pk, topic.topic) for topic in Topic.objects.all()]
        choices = [custom_topics[0]] + choices + [custom_topics[1]]
        self.fields['topic'].choices = choices

    def clean(self):
        # honeypot detection
        cleaned_data = super().clean()
        phone_no = cleaned_data.get("phone_no")
        if len(phone_no) != 0:
            try:
                message = cleaned_data.get('message')
                msg = message.replace('\n', ' ').replace('\r', '')
            except Exception:
                msg = "(no message)"

            logger.warning("Email attempt using honeypot: '{}'".format(msg))
            raise forms.ValidationError(
                "Sorry, something went wrong. "
                "Please try again, or send us an email.")

    def send_email(self):
        # get posted topic id
        # create list of custom topic keys
        # ascertain whether selected topic is from db or custom list
        topic = self.cleaned_data['topic']
        contactless_topics = [
            custom_topic[0] for custom_topic in custom_topics
        ]
        topic = None if topic in contactless_topics else topic

        # if posted topic id is from db rather than custom list,
        # retrieve its corresponding 'topic' field from its model
        # also extract which additional contacts to send email to
        if topic:
            topic_model = Topic.objects.get(pk=topic)
            topic_label = topic_model.topic
            contacts = topic_model.contact.values_list('email', flat=True)
            additional_recipients = list(contacts)
        else:
            topic_label = 'General/Misc'
            additional_recipients = []

        subject = '{} - Website message received'.format(settings.SITE_TITLE)
        email_from = settings.CONTACT_EMAIL
        email_to = [settings.CONTACT_EMAIL] + additional_recipients
        message = ('Website message received on:\n{0}\n\n'
                   'From:\n{1}\n\n'
                   'Email:\n{2}\n\n'
                   'Topic:\n{3}\n\n'
                   'Message:\n{4}\n\n'
                   '-----------------------------------\n\n').format(
                       timezone.now(),
                       self.cleaned_data['name'],
                       self.cleaned_data['email'],
                       topic_label,
                       self.cleaned_data['message'],
                   )

        try:
            send_mail(subject, message, email_from, email_to)
        except BadHeaderError:
            logger.warning("Contact email, invalid header found: '{}'".format(
                self.cleaned_data['message']))
            return HttpResponse('Invalid header found.')
        except Exception as e:
            logger.warning("Contact email, general error: '{}'".format(e))
