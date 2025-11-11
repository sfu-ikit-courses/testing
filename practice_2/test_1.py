import pytest
from lab2 import ClassUnderTest, ClassUnderTest2, AffectingClass


@pytest.mark.parametrize("val,arg,expected", [
    (5, 3, 5),   # val > arg → val
    (2, 5, 5),   # val < arg → arg
    (4, 4, 4),   # val == arg → arg
])
def test_public_method(val, arg, expected):
    aff = AffectingClass()
    aff.val = val
    cut = ClassUnderTest(aff)
    assert cut.public_method(arg) == expected


@pytest.mark.parametrize("return_value", [0, 1, 42])
def test_call_affecting_method(return_value):
    class StubAffectingClass(AffectingClass):
        def method(self):
            return return_value

    aff = StubAffectingClass()
    cut2 = ClassUnderTest2(aff)
    assert cut2.call_affecting_method() == return_value
