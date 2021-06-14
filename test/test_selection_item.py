import pytest

# noinspection PyProtectedMember
from cursesmenu.items.selection_item import SelectionItem


@pytest.fixture
def selection_item():
    yield SelectionItem("item", 1)


def test_selection_item(selection_item: SelectionItem):
    assert selection_item.get_return() == 1
