import unittest
from unittest.mock import MagicMock
from lab2 import ClassUnderTest


class TestWithSetup(unittest.TestCase):
    def setUp(self):
        self.mock_aff = MagicMock()
        self.mock_aff.val = 7
        self.cut = ClassUnderTest(self.mock_aff)

    def test_public_method_with_mock(self):
        result = self.cut.public_method(5)
        self.assertEqual(result, 7)


def test_public_method_with_mock_no_setup():
    mock_aff = MagicMock()
    mock_aff.val = 10
    cut = ClassUnderTest(mock_aff)
    assert cut.public_method(5) == 10
