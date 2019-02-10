from django.conf import settings
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.html import strip_tags


def save_news(sender, instance, created, **kwargs):
    if created:
        url = get_news_url(instance)
        save('News', instance.title, url)


def save_results(sender, instance, created, **kwargs):
    if created:
        url = get_results_url(instance)
        save('Results', instance.fixture.title, url)


def save_announcements(sender, instance, created, **kwargs):
    if created:
        url = get_announcements_url()
        # shorten annoucement to tweet length if necessary
        announcement = instance.announcement
        announcement = strip_tags(announcement)
        announcement = truncatechars(announcement, 120)
        # don't re-post announcements - they may no longer be relevant
        save('Notice', announcement, url, True)


def save(model, title, url, reposted=False):
    from .models import Social
    social = Social(model=model, title=title, url=url, reposted=reposted)
    social.save()
    social.post()


def get_news_url(obj):
    url = reverse('news-detail', kwargs={'pk': obj.id, 'slug': obj.slug})
    return '{0}{1}'.format(settings.HOST, url)


def get_results_url(obj):
    url = reverse('results-index')
    return '{0}{1}'.format(settings.HOST, url)


def get_announcements_url():
    return settings.HOST
