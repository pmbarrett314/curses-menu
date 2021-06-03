import pytest

# noinspection PyProtectedMember
from cursesmenu.curses_menu import _SelectionItem


@pytest.fixture
def selection_item():
    yield _SelectionItem("item", 1)


def test_selection_item(selection_item: _SelectionItem):
    assert selection_item.get_return() == 1
