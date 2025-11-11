from unittest.mock import MagicMock, PropertyMock
from lab2 import ClassUnderTest


def test_val_property_called():
    mock_aff = MagicMock()

    prop = PropertyMock(return_value=10)
    type(mock_aff).val = prop

    cut = ClassUnderTest(mock_aff)
    _ = cut.public_method(5)

    assert prop.call_count > 0, "Свойство val не было вызвано"
