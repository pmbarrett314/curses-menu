from unittest import mock

import pytest

from cursesmenu import CursesMenu

pytestmark = pytest.mark.usefixtures("mock_cursesmenu_curses", "mock_clear")


def test_get_selection():
    with mock.patch("cursesmenu.curses_menu.CursesMenu.get_input") as f:
        f.return_value = ord("\n")
        assert CursesMenu.get_selection(["thing1", "thing2"], "title", "subtitle") == 0
