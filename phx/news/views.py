import logging
from datetime import datetime

from components.models import COMPONENT_TYPES
from django.db.models import Q
from django.urls import reverse
from django.views import generic

from .models import Component, News

logger = logging.getLogger(__name__)


class NewsListView(generic.ListView):
    model = News

    def calculate_year_range(self):
        return reversed(range(2009, datetime.now().year + 1))

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['breadcrumb'] = self.generate_breadcrumb()
        context['search'] = self.request.GET.get('search', '')
        context['page_title'] = 'News'
        context['year_range'] = self.calculate_year_range()
        context['filter_form_url'] = reverse('news-list')
        context['paginate_by'] = self.paginate_by

        year = self.request.GET.get('year', '')
        if year:
            context['year'] = int(year)

        return context

    def get_queryset(self):
        query = News.objects.select_related('thumbnail').all().distinct()

        search = self.request.GET.get('search')
        if search:
            query = query.filter(
                Q(title__icontains=search) | Q(summary__icontains=search)
                | Q(components__editorial__content__icontains=search)
                | Q(components__table__content__icontains=search))

        year = self.request.GET.get('year', '')
        year_range = self.calculate_year_range()
        if year and int(year) in year_range:
            query = query.filter(created_date__year=year)

        return query

    def generate_breadcrumb(self):
        return [{
            'title': 'Home',
            'linkUrl': '/',
        }, {
            'title': 'News',
        }]

    def get_paginate_by(self, queryset):
        pagination_options = [10, 50]
        self.paginate_by = pagination_options[0]
        requested_page_size = self.request.GET.get(
            'pageSize',
            self.paginate_by,
        )
        try:
            paginate_by = int(requested_page_size)
        except Exception as e:
            logger.warning(
                "Results pagination int value issue: '{}'".format(e))
        if 'paginate_by' in locals() and paginate_by in pagination_options:
            self.paginate_by = paginate_by
        return self.paginate_by


class NewsDetailView(generic.DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)

        id = self.object.id
        context['components'] = Component.objects.select_related(
            *COMPONENT_TYPES).filter(news_id=id)

        context['breadcrumb'] = self.generate_breadcrumb()
        context['data'] = {
            "previous": self.get_previous(),
            "next": self.get_next(),
        }
        context['page_title'] = 'News'
        return context

    def get_previous(self):
        id = self.object.id
        previous = News.objects.filter(id__lt=id).order_by('-id')[0:1].first()
        if previous:
            return {
                'title':
                previous.title,
                'link_url':
                reverse('news-detail',
                        kwargs={
                            'pk': previous.id,
                            'slug': previous.slug
                        })
            }

    def get_next(self):
        id = self.object.id
        next = News.objects.filter(id__gt=id).order_by('id')[0:1].first()
        if next:
            return {
                'title':
                next.title,
                'link_url':
                reverse('news-detail',
                        kwargs={
                            'pk': next.id,
                            'slug': next.slug
                        })
            }

    def generate_breadcrumb(self):
        breadcrumb = [{
            'title': 'Home',
            'linkUrl': '/',
        }, {
            'title': 'News',
            'linkUrl': reverse('news-list'),
        }, {
            'title': self.object.title
        }]
        return breadcrumb
