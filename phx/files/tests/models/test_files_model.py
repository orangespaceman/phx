from unittest.mock import Mock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models import file_size_validator


class TestFilesModel(TestCase):

    @patch('files.models.ValidationError')
    def test_validation_pass(self, validation_error):
        """
        File size validation pass
        """
        file_mock = Mock()
        file_mock.size = 10 * 1024 * 1024
        file_size_validator(file_mock)

        validation_error.assert_not_called()

    def test_validation_fail(self):
        """
        File size validation fail
        """
        file_mock = Mock()
        file_mock.size = 10 * 1024 * 1024 + 1

        self.assertRaises(ValidationError, file_size_validator, file_mock)
