import random
from itertools import chain

from components.models import COMPONENT_TYPES
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic
from fixtures.models import Fixture
from news.models import News
from pages.models import Component, Page
from results.models import Result

from .models import Announcement, Content, Hero, HeroImageCategory


class HomeView(generic.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        self.content = Content.objects.first()
        context = super(HomeView, self).get_context_data(**kwargs)

        page = get_object_or_404(Page, slug='/home/')
        context['page'] = page
        context['page_title'] = page.title
        context['components'] = Component.objects.select_related(
            *COMPONENT_TYPES).filter(page_id=page.id)

        context['about'] = self.get_about()
        context['announcement'] = self.get_announcement()
        context['fixtures'] = self.get_fixtures()
        context['gallery'] = self.get_gallery()
        context['heroes'] = self.get_heroes()
        context['join'] = self.get_join()
        context['news'] = self.get_news()
        context['results'] = self.get_results()
        context['title'] = self.get_title()
        return context

    def get_about(self):
        return self.content.about

    def get_announcement(self):
        annoucement = Announcement.objects.filter(
            display_until__gte=timezone.now()).order_by(
                '-created_date')[:1].first()
        if annoucement:
            return annoucement.announcement

    def get_fixtures(self):
        return Fixture.objects.filter(
            event_date__gte=timezone.now()).order_by('event_date')[:5]

    def get_gallery(self):
        return self.content.gallery

    def get_heroes(self):
        """
        Select the desired number of hero images for each category
        Ensure each query excludes hero images that have already been returned
        """
        categories = HeroImageCategory.objects.all()
        heroes = []
        exclude_ids = []
        for category in categories:
            queryset = Hero.objects.filter(
                image_categories=category).order_by('?').exclude(
                    id__in=exclude_ids)[:category.count]
            exclude_ids = exclude_ids + [hero.id for hero in queryset]
            heroes = chain(heroes, queryset)
        hero_list = list(heroes)
        random.shuffle(hero_list)
        return hero_list

    def get_join(self):
        return self.content.join

    def get_news(self):
        return News.objects.select_related('thumbnail').all().order_by(
            '-created_date')[:3]

    def get_results(self):
        return Result.objects.filter(event_date__lte=timezone.now(),
                                     draft=False).order_by('-event_date')[:5]

    def get_title(self):
        return self.content.title
