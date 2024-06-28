from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django_extensions.management.jobs import WeeklyJob
from results.results_processor import ResultsProcessor


class Job(WeeklyJob):
    help = "Prepare results spreadsheet for manual entry."

    def execute(self):
        [curr_file, prev_file] = ResultsProcessor.fetch_results(2)

        processor = ResultsProcessor()
        num_new_results = processor.process(curr_file, prev_file)

        if num_new_results > 0:
            filename = datetime.today().strftime(
                "results/NewResults_%Y-%m-%d.xlsx")
            processor.save(filename)

            self._send_email(num_new_results, filename)

    def _send_email(self, num_new_results, filename):
        subject = '{} - New results ready'.format(settings.SITE_TITLE)
        email_from = settings.CONTACT_EMAIL
        # TODO: add results crew topic
        email_to = [settings.CONTACT_EMAIL]
        message = ("New results are ready for upload\n\n"
                   "Number of new results: {}\n\n"
                   "File: https://brightonphoenix.org.uk/{}\n\n"
                   "-----------------------------------\n\n").format(
                       num_new_results, filename)

        send_mail(subject, message, email_from, email_to)
