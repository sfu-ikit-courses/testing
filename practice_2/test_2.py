import pytest
from lab2 import ClassUnderTest, AffectingClass


def test_protected_method_returns_val():
    aff = AffectingClass()
    aff.val = 10
    cut = ClassUnderTest(aff)
    assert cut.protected_method(5) == 10


def test_protected_method_raises_exception():
    aff = AffectingClass()
    cut = ClassUnderTest(aff)
    with pytest.raises(ValueError, match="arg is equal to zero"):
        cut.protected_method(0)
