from django.test import TestCase

from ...helpers.file import file_size_string


class TestHelperFile(TestCase):

    def test_file_size_string_kb(self):
        """
        Return kb string
        """
        results = file_size_string(511999)
        self.assertEqual(results, '500.0 kb')

    def test_file_size_string_mb(self):
        """
        Return mb string
        """
        results = file_size_string(4194303999)
        self.assertEqual(results, '4000.0 mb')

    def test_file_size_string_gb(self):
        """
        Return gb string
        """
        results = file_size_string(4194304000)
        self.assertEqual(results, '3.91 gb')
