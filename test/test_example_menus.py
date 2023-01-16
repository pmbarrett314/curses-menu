import test.example_menus.basic_menu
import test.example_menus.menu_with_items
import test.example_menus.menu_with_lots_of_items
import test.example_menus.zero_padded_menu_with_lots_of_items

import pytest

pytestmark = pytest.mark.usefixtures("mock_cursesmenu_curses", "mock_clear")


def test_basic_menu(mock_cursesmenu_curses):
    mock_cursesmenu_curses.mock_window.getch.side_effect = lambda: ord("\n")
    test.example_menus.basic_menu.main()


def test_menu_with_items(mock_cursesmenu_curses):
    mock_cursesmenu_curses.mock_window.getch.side_effect = lambda: ord("\n")
    test.example_menus.menu_with_items.main()


def test_menu_with_lots_of_items(mock_cursesmenu_curses):
    mock_cursesmenu_curses.mock_window.getch.side_effect = lambda: ord("\n")
    test.example_menus.menu_with_lots_of_items.main()


def test_zero_padded_menu_with_lots_of_items(mock_cursesmenu_curses):
    mock_cursesmenu_curses.mock_window.getch.side_effect = lambda: ord("\n")
    test.example_menus.zero_padded_menu_with_lots_of_items.main()
