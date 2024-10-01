import logging
from datetime import datetime

from components.models import COMPONENT_TYPES
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from fixtures.models import Category
from pages.models import Component, Page

from phx.helpers.subnav import generate_subnav

from .models import Athlete, Result

logger = logging.getLogger(__name__)


class ResultsListView(generic.ListView):
    model = Result

    def calculate_year_range(self):
        return reversed(range(2009, datetime.now().year + 1))

    def get_context_data(self, **kwargs):
        context = super(ResultsListView, self).get_context_data(**kwargs)
        context['breadcrumb'] = self.generate_breadcrumb()
        page = get_object_or_404(Page, slug=self.request.path)
        context['page'] = page
        context['page_title'] = page.title
        context['components'] = Component.objects.select_related(
            *COMPONENT_TYPES).filter(page_id=page.id)
        context['categories'] = Category.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['order'] = self.request.GET.get('order', '')
        context['category'] = self.request.GET.get('category', '')
        context['subnav'] = generate_subnav(self.request.path, context['page'])
        context['year_range'] = self.calculate_year_range()
        context['filter_form_url'] = reverse('results-index')
        context['paginate_by'] = self.paginate_by

        year = self.request.GET.get('year', '')
        if year:
            context['year'] = int(year)

        return context

    def get_queryset(self):
        query = Result.objects.prefetch_related(
            'categories', 'event_set__performance_set__athlete').filter(
                event_date__lte=timezone.now(), draft=False)

        search = self.request.GET.get('search')
        if search:
            athletes = Athlete.objects.annotate(full_name=Concat(
                'first_name', Value(' '), 'last_name')).filter(
                    full_name__icontains=search)

            query = query.filter(
                Q(summary__icontains=search)
                | Q(results__icontains=search)
                | Q(title__icontains=search)
                | Q(categories__abbreviation__icontains=search)
                | Q(categories__title__icontains=search)
                | Q(event__location__icontains=search)
                | Q(event__name__icontains=search)
                | Q(event__performance__athlete__in=athletes))

        category = self.request.GET.get('category')
        if category:
            query = query.filter(categories__abbreviation=category)

        year = self.request.GET.get('year', '')
        year_range = self.calculate_year_range()
        if year and int(year) in year_range:
            query = query.filter(event_date__year=year)

        order = self.request.GET.get('order', '')
        if order and order == 'date-added':
            query = query.order_by('-created_date').distinct()
        else:
            query = query.order_by('-event_date').distinct()

        return query

    def generate_breadcrumb(self):
        return [{
            'title': 'Home',
            'linkUrl': '/',
        }, {
            'title': 'Results',
        }]

    def get_paginate_by(self, queryset):
        pagination_options = [10, 50]
        self.paginate_by = pagination_options[1]
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
