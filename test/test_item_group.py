import pytest

from cursesmenu import CursesMenu
from cursesmenu.item_group import ItemGroup
from cursesmenu.items import MenuItem


@pytest.fixture
def sample_items():
    item0 = MenuItem("item0")
    item1 = MenuItem("item1")
    return [item0, item1]


@pytest.fixture
def sample_menu(sample_items, mock_cursesmenu_curses_vary_window_size):
    menu = CursesMenu("menu", "TestSampleMenu")
    menu.items.append(sample_items[0])
    menu.items.append(sample_items[1])
    menu.start()
    menu.wait_for_start(timeout=10)
    yield menu
    menu.exit()
    menu.join(timeout=10)


@pytest.fixture
def sample_item_list(sample_menu):
    return ItemGroup(sample_menu, sample_menu.items)


def test_init(sample_menu):
    item_list_1 = ItemGroup(sample_menu, sample_menu.items)
    item_list_2 = ItemGroup(sample_menu, None)

    assert item_list_1.menu == sample_menu
    assert item_list_2.menu == sample_menu


def test_single_item_methods(sample_item_list, sample_menu):
    new_item = MenuItem("Item 3")
    sample_item_list[0] = new_item
    assert sample_item_list[0] is new_item
    assert new_item.menu is sample_menu
    sample_item_list.append(new_item)
    assert sample_item_list[-1] is new_item
    del sample_item_list[-1]
    assert sample_item_list[-1] is not new_item


def test_slice_methods(sample_item_list, sample_menu):
    assert sample_item_list[0:2] == ItemGroup(
        sample_menu,
        [sample_item_list[0], sample_item_list[1]],
    )
    new_item_1 = MenuItem("Item 4")
    new_item_2 = MenuItem("Item 5")
    new_items = [new_item_1, new_item_2]
    sample_item_list[0:1] = new_items


def test_eq(sample_item_list):
    assert sample_item_list != 1

    item_list_2 = ItemGroup(None, sample_item_list.items)
    assert sample_item_list != item_list_2
    new_item = MenuItem("Item 6")
    item_list_3 = ItemGroup(
        sample_item_list.menu,
        [sample_item_list[0], sample_item_list[1], new_item],
    )
    assert sample_item_list != item_list_3

    item_list_4 = ItemGroup(sample_item_list.menu, [sample_item_list[0], new_item])
    assert sample_item_list != item_list_4

    item_list_5 = ItemGroup(
        sample_item_list.menu,
        [sample_item_list[0], sample_item_list[1]],
    )

    assert sample_item_list == item_list_5
