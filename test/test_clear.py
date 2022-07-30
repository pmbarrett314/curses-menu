import sys
from unittest import mock

import cursesmenu as cursesmenu
import cursesmenu.utils


def test_clear():
    tmp_platform = sys.platform
    sys.platform = "win32"
    with mock.patch("cursesmenu.utils.os.system") as mock_system:
        cursesmenu.utils.clear_terminal()
        mock_system.assert_called_once_with("cls")
    sys.platform = "linux"
    with mock.patch("cursesmenu.utils.os.system") as mock_system:
        cursesmenu.utils.clear_terminal()
        mock_system.assert_called_once_with("reset")
    sys.platform = tmp_platform
