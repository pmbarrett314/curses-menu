import pytest

from cursesmenu.items import FunctionItem

pytestmark = pytest.mark.usefixtures(
    "mock_cursesmenu_curses",
    "mock_clear",
    "mock_externalitem_curses",
)


def get_two():
    return 2


def add(two, two_two):
    return two + two_two


def test_basic_function():
    item = FunctionItem("get_two", get_two)
    item.action()
    assert item.get_return() == 2


def test_function_with_args():
    item = FunctionItem("add", add, args=[2], kwargs={"two_two": 2})
    item.action()
    assert item.get_return() == 4
