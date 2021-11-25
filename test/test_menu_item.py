import pytest

from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


@pytest.fixture
def basic_item():
    yield MenuItem("item")


@pytest.fixture
def item_with_menu():
    menu = CursesMenu()
    yield MenuItem("item with menu", menu=menu)


def test_str(basic_item: MenuItem):
    assert str(basic_item) == " item"


def test_return(basic_item: MenuItem):
    assert basic_item.get_return() is None


def test_return_with_menu(item_with_menu: MenuItem):
    assert item_with_menu.get_return() is None


def test_show(basic_item: MenuItem):
    assert basic_item.show("1") == "1 - item"


def test_set_up(basic_item: MenuItem):
    basic_item.set_up()


def test_action(basic_item: MenuItem):
    basic_item.action()


def test_clean_up(basic_item: MenuItem):
    basic_item.clean_up()
