from django.test import TestCase, override_settings
from unittest.mock import patch

from ...models import Topic, Contact
from ...forms import ContactForm


@patch('contact.forms.send_mail')
@override_settings(CONTACT_EMAIL='test@test.com')
class TestContactForm(TestCase):
    def test_send_email(self, send_mail):
        """
        Send email with preset topic to default contact
        """
        topic = 'misc'
        contact_form = ContactForm()
        contact_form.cleaned_data = {
            'name': 'Lorem Ipsum',
            'email': 'lorem@ipsum.com',
            'topic': topic,
            'message': 'This is a test',
        }
        contact_form.send_email()

        send_mail.assert_called_once()
        self.assertEqual(send_mail.call_args[0][3], ['test@test.com'])

    def test_send_email_custom_topic(self, send_mail):
        """
        Send email with custom topic to custom contacts
        """
        contact1 = Contact.objects.create(name='lorem', email='a@lorem.com')
        contact2 = Contact.objects.create(name='ipsum', email='a@ipsum.com')
        topic = Topic.objects.create(topic='Test topic')
        topic.contact.add(contact1)
        topic.contact.add(contact2)

        contact_form = ContactForm()
        contact_form.cleaned_data = {
            'name': 'Lorem Ipsum',
            'email': 'lorem@ipsum.com',
            'topic': '1',
            'message': 'This is a test',
        }
        contact_form.send_email()

        send_mail.assert_called_once()
        self.assertEqual(send_mail.call_args[0][3], [
            'test@test.com',
            'a@lorem.com',
            'a@ipsum.com',
        ])