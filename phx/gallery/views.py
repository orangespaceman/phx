import logging
from datetime import datetime

from django.db.models import Q
from django.urls import reverse
from django.views import generic

from .models import Gallery, Image

logger = logging.getLogger(__name__)


class GalleryListView(generic.ListView):
    model = Gallery

    def calculate_year_range(self):
        return reversed(range(2009, datetime.now().year + 1))

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['breadcrumb'] = self.generate_breadcrumb()
        context['search'] = self.request.GET.get('search', '')
        context['page_title'] = 'Gallery'
        context['year_range'] = self.calculate_year_range()
        context['filter_form_url'] = reverse('gallery-list')
        context['paginate_by'] = self.paginate_by

        year = self.request.GET.get('year', '')
        if year:
            context['year'] = int(year)

        return context

    def get_queryset(self):
        query = Gallery.objects.select_related('thumbnail').prefetch_related(
            'images').all().distinct()

        search = self.request.GET.get('search')
        if search:
            query = query.filter(
                Q(title__icontains=search) | Q(summary__icontains=search))

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
            'title': 'Gallery',
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


class GalleryDetailView(generic.DetailView):
    model = Gallery

    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)

        id = self.object.id
        context['images'] = Image.objects.filter(gallery_id=id)

        context['breadcrumb'] = self.generate_breadcrumb()
        context['data'] = {
            "previous": self.get_previous(),
            "next": self.get_next(),
        }
        context['page_title'] = 'Gallery'
        return context

    def get_previous(self):
        id = self.object.id
        previous = Gallery.objects.filter(
            id__lt=id).order_by('-id')[0:1].first()
        if previous:
            return {
                'title':
                previous.title,
                'link_url':
                reverse('gallery-detail',
                        kwargs={
                            'pk': previous.id,
                            'slug': previous.slug
                        })
            }

    def get_next(self):
        id = self.object.id
        next = Gallery.objects.filter(id__gt=id).order_by('id')[0:1].first()
        if next:
            return {
                'title':
                next.title,
                'link_url':
                reverse('gallery-detail',
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
            'title': 'Gallery',
            'linkUrl': reverse('gallery-list'),
        }, {
            'title': self.object.title
        }]
        return breadcrumb
