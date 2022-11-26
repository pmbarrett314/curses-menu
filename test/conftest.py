import sys
import unittest.mock as mock

if not sys.platform.startswith("win"):  # pragma: no cover all
    import curses
else:  # pragma: no cover all
    curses = None

import pytest

# noinspection PyUnresolvedReferences
import cursesmenu.curses_menu  # noqa: F401


@pytest.fixture()
def mock_clear():
    with mock.patch("cursesmenu.utils.clear_terminal") as f:
        with mock.patch("cursesmenu.utils.soft_clear_terminal") as g:
            yield f, g


@pytest.fixture(params=[3, 99999999])
def window_rows(request):
    return request.param


@pytest.fixture(params=[10, 99999999])
def window_cols(request):
    return request.param


def mock_curses_(rows, cols):
    f = mock.MagicMock(spec=curses)
    f.mock_window = mock.MagicMock(
        spec=[
            "keypad",
            "addstr",
            "border",
            "getch",
            "refresh",
            "clear",
            "getmaxyx",
            "resize",
        ],
    )

    f.mock_window.getch.side_effect = lambda: 0
    f.mock_window.getmaxyx.return_value = (rows, cols)

    def wrapper(function, *args, **kwargs):  # pragma: no cover all
        return function(f.mock_window, *args, **kwargs)

    f.initscr.return_value = f.mock_window
    f.newpad.return_value = f.mock_window
    f.wrapper = wrapper

    return f


@pytest.fixture
def mock_curses_window_size(window_rows, window_cols):
    return mock_curses_(window_rows, window_cols)


@pytest.fixture
def mock_curses():
    return mock_curses_(99999999, 99999999)


@pytest.fixture()
def mock_cursesmenu_curses(mock_curses):
    with mock.patch("cursesmenu.curses_menu.curses", new=mock_curses) as f:
        yield f


@pytest.fixture()
def mock_cursesmenu_curses_vary_window_size(mock_curses_window_size):
    with mock.patch("cursesmenu.curses_menu.curses", new=mock_curses_window_size) as f:
        yield f


@pytest.fixture()
def mock_externalitem_curses(mock_curses):
    with mock.patch("cursesmenu.items.external_item.curses", new=mock_curses) as f:
        yield f
