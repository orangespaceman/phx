import pytest
from django.test import TestCase
from django.urls import reverse

from ..factories import GalleryFactory, ImageFactory


# Remove once https://github.com/SmileyChris/easy-thumbnails/pull/626 is done
@pytest.mark.filterwarnings(
    "ignore::django.utils.deprecation.RemovedInDjango51Warning")
class TestGalleryDetailView(TestCase):

    def test_url_resolves(self):
        """"
        URL resolves as expected
        """
        gallery = GalleryFactory(title='this? is& a! (test*)')
        url = reverse('gallery-detail',
                      kwargs={
                          'pk': gallery.id,
                          'slug': gallery.slug
                      })

        self.assertEqual(url, '/gallery/{}/this-is-a-test/'.format(gallery.id))

    def test_get(self):
        """"
        GET request uses template
        """
        gallery = GalleryFactory(title='this? is& a! (test*)')
        url = reverse('gallery-detail',
                      kwargs={
                          'pk': gallery.id,
                          'slug': gallery.slug
                      })

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery_detail.html')

    def test_get_no_gallery(self):
        """"
        GET request returns a 404 when no gallery found
        """
        url = reverse('gallery-detail',
                      kwargs={
                          'pk': 9999,
                          'slug': 'this is a test'
                      })

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_previous_next(self):
        """"
        GET request returns previous and next gallerys
        """
        gallery_1 = GalleryFactory(title='gallery 1')
        gallery_2 = GalleryFactory(title='gallery 2')
        gallery_3 = GalleryFactory(title='gallery 3')
        url = reverse('gallery-detail',
                      kwargs={
                          'pk': gallery_2.id,
                          'slug': gallery_2.slug
                      })

        response = self.client.get(url)
        self.assertEqual(response.context['gallery'], gallery_2)
        self.assertEqual(
            response.context['data']['previous']['link_url'],
            '/gallery/{}/{}/'.format(gallery_1.id, gallery_1.slug))
        self.assertEqual(
            response.context['data']['next']['link_url'],
            '/gallery/{}/{}/'.format(gallery_3.id, gallery_3.slug))

    def test_gallery_images(self):
        """"
        GET request returns images as expected
        """
        gallery = GalleryFactory()
        first_image = ImageFactory(caption='first image',
                                   gallery=gallery,
                                   order=1)
        ImageFactory.create_batch(4, gallery=gallery, order=2)

        url = reverse('gallery-detail',
                      kwargs={
                          'pk': gallery.id,
                          'slug': gallery.slug
                      })

        response = self.client.get(url)
        gallery_instance = response.context['gallery']
        first_image_instance = gallery_instance.images.first()
        self.assertEqual(gallery_instance.images.count(), 5)
        self.assertEqual(first_image_instance, first_image)
        self.assertEqual(first_image_instance.caption, 'first image')
