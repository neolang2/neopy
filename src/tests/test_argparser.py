import unittest
from unittest import mock
import random
import string

import main
import constants


class TestArgParser(unittest.TestCase):
    def __random_filename(self):
        return ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=constants.UNITTEST_FILENAME_LENGTH)) + "." + constants.EXTENSION

    def test_six_files(self):
        filenames = [self.__random_filename()
                     for _ in range(6)]
        found_filenames = []

        # Make sure argparse checks all generated files
        def mock_open(in_filename, in_mode, *args, **kwargs):
            self.assertIn(in_filename, filenames)
            self.assertEqual(in_mode, "r")
            found_filenames.append(in_filename)
            return unittest.mock.MagicMock()
        main.argparse.open = mock_open
        main.parse_args(filenames)
        self.assertEqual(found_filenames, filenames)
