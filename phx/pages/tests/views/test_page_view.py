from factory import SubFactory
from django.test import TestCase
from django.urls import reverse

from ..factories import (
    PageFactory,
    ComponentFactory,
    EditorialFactory,
    FeatureFactory,
    QuoteFactory,
    ImageFactory,
    ListItemsFactory,
)


class TestPageView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        page = PageFactory(title='this? is& a! (test*)')
        url = reverse(
            'page-detail', kwargs={'slug': page.get_slug()}
        )

        self.assertEqual(url, '/this-is-a-test/')

    def test_get(self):
        """"
        GET request uses template
        """
        page = PageFactory(title='this? is& a! (test*)')
        url = reverse(
            'page-detail', kwargs={'slug': page.get_slug()}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/page.html')

    def test_get_no_article(self):
        """"
        GET request returns a 404 when no article found
        """
        url = reverse(
            'page-detail', kwargs={'slug': 'this is a test'}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_component_editorial(self):
        """"
        GET request returns editorial component as expected
        """
        page = PageFactory()
        editorial = EditorialFactory(
            title='first editorial block',
            component=SubFactory(ComponentFactory, page=page))

        url = reverse(
            'page-detail', kwargs={'slug': page.get_slug()}
        )

        response = self.client.get(url)
        component = response.context['components'].first()
        first_editorial = component.editorial
        self.assertEqual(first_editorial, editorial)
        self.assertEqual(first_editorial.title, 'first editorial block')

    def test_component_feature(self):
        """"
        GET request returns feature component as expected
        """
        page = PageFactory()
        feature = FeatureFactory(
            title='first feature block',
            component=SubFactory(ComponentFactory, page=page))

        url = reverse(
            'page-detail', kwargs={'slug': page.get_slug()}
        )

        response = self.client.get(url)
        component = response.context['components'].first()
        first_feature = component.feature
        self.assertEqual(first_feature, feature)
        self.assertEqual(first_feature.title, 'first feature block')

    def test_component_quote(self):
        """"
        GET request returns quote component as expected
        """
        page = PageFactory()
        quote = QuoteFactory(
            quote='first quote block',
            component=SubFactory(ComponentFactory, page=page))

        url = reverse(
            'page-detail', kwargs={'slug': page.get_slug()}
        )

        response = self.client.get(url)
        component = response.context['components'].first()
        first_quote = component.quote
        self.assertEqual(first_quote, quote)
        self.assertEqual(first_quote.quote, 'first quote block')

    def test_component_image(self):
        """"
        GET request returns image component as expected
        """
        page = PageFactory()
        image = ImageFactory(
            caption='first image block',
            component=SubFactory(ComponentFactory, page=page))

        url = reverse(
            'page-detail', kwargs={'slug': page.get_slug()}
        )

        response = self.client.get(url)
        component = response.context['components'].first()
        first_image = component.image
        self.assertEqual(first_image, image)
        self.assertEqual(first_image.caption, 'first image block')

    def test_component_list_items(self):
        """"
        GET request returns list_items component as expected
        """
        page = PageFactory()
        list_items = ListItemsFactory(
            title_1='first list_items block',
            component=SubFactory(ComponentFactory, page=page))

        url = reverse(
            'page-detail', kwargs={'slug': page.get_slug()}
        )

        response = self.client.get(url)
        component = response.context['components'].first()
        first_list_items = component.list_items
        self.assertEqual(first_list_items, list_items)
        self.assertEqual(first_list_items.title_1, 'first list_items block')