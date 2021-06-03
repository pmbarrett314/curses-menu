import sys
from unittest import mock

import cursesmenu as cursesmenu


def test_clear():
    sys.platform = "win32"
    with mock.patch("cursesmenu.curses_menu.os.system") as mock_system:
        cursesmenu.curses_menu.clear_terminal()
        mock_system.assert_called_once_with("cls")
    sys.platform = "linux"
    with mock.patch("cursesmenu.curses_menu.os.system") as mock_system:
        cursesmenu.curses_menu.clear_terminal()
        mock_system.assert_called_once_with("reset")
