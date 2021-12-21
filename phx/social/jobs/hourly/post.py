from django_extensions.management.jobs import HourlyJob

from ...models import Social


class Job(HourlyJob):
    help = "Post to social media."

    def execute(self):
        social = Social()
        social.post()
