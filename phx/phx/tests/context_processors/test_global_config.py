from django.test import override_settings, TestCase

from ...context_processors.global_config import global_config


class TestContextProcessorGlobalConfig(TestCase):

    def test_global_config(self):
        """
        Return settings in config object
        """
        results = global_config({})
        self.assertEqual(results['HOST'], 'http://example.com')
        self.assertTrue('ANALYTICS' not in results)

    @override_settings(ANALYTICS=1234)
    def test_global_config_analytics(self):
        """
        Return analytics settings in config object
        """
        results = global_config({})
        self.assertEqual(results['ANALYTICS'], 1234)
