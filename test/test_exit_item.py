import pytest

from cursesmenu import CursesMenu
from cursesmenu.items import ExitItem, SubmenuItem


@pytest.fixture
def exit_item():
    return ExitItem()


@pytest.fixture
def exit_item_with_parent():
    root_menu = CursesMenu("root_menu")
    submenu = CursesMenu("submenu")

    submenu_item = SubmenuItem("submenu_item_1", submenu, menu=root_menu)
    root_menu.items.append(submenu_item)
    return submenu.end_items[0]


def test_show(exit_item):
    assert exit_item.show("q") == "q - Exit"


def test_show_with_parent(exit_item_with_parent):
    assert exit_item_with_parent.show("q") == "q - Return to root_menu menu"
