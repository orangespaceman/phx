from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import save_announcements, save_gallery, save_news, save_results


class SocialConfig(AppConfig):
    name = 'social'

    def ready(self):
        from news.models import News
        from results.models import Result
        from gallery.models import Gallery
        from home.models import Announcement

        post_save.connect(save_news, sender=News, dispatch_uid="add_news")
        post_save.connect(save_results,
                          sender=Result,
                          dispatch_uid="add_results")
        post_save.connect(save_gallery,
                          sender=Gallery,
                          dispatch_uid="add_gallery")
        post_save.connect(save_announcements,
                          sender=Announcement,
                          dispatch_uid="add_announcements")
