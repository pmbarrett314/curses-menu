from typing import List

import pytest

from cursesmenu import CursesMenu
from cursesmenu.items import ExitItem, MenuItem

pytestmark = pytest.mark.usefixtures("mock_cursesmenu_curses", "mock_clear")


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
def empty_menu():
    menu = CursesMenu("menu", "empty menu", show_exit_item=False)
    menu.start()
    menu.wait_for_start(timeout=10)
    yield menu
    menu.exit()
    menu.join(timeout=10)


@pytest.fixture
def big_menu():
    menu = CursesMenu("Test Menu")
    for i in range(100):
        menu.items.append(MenuItem("item{}".format(i), should_exit=True))
    menu.start()
    menu.wait_for_start(timeout=10)
    yield menu
    menu.exit()
    menu.join(timeout=10)


def test_empty_menu(empty_menu: CursesMenu):
    assert empty_menu.current_item is None
    assert empty_menu.selected_item is None
    empty_menu.select()
    empty_menu.go_to_exit()
    empty_menu.join(timeout=10)
    assert not empty_menu.is_alive()


def test_big_menu(big_menu: CursesMenu):
    pass


def test_go_down(sample_menu: CursesMenu, sample_items: List[MenuItem]):
    sample_menu.go_down()
    assert sample_menu.current_option == 1
    assert sample_menu.current_item is sample_items[1]
    sample_menu.go_down()
    assert sample_menu.current_option == 2
    assert type(sample_menu.current_item) == ExitItem
    sample_menu.go_down()
    assert sample_menu.current_option == 0
    assert sample_menu.current_item is sample_items[0]


def test_go_up(sample_menu: CursesMenu, sample_items: List[MenuItem]):
    sample_menu.go_up()
    assert sample_menu.current_option == 2
    assert type(sample_menu.current_item) == ExitItem
    sample_menu.go_up()
    assert sample_menu.current_option == 1
    assert sample_menu.current_item is sample_items[1]
    sample_menu.go_up()
    assert sample_menu.current_option == 0
    assert sample_menu.current_item is sample_items[0]


def test_go_to(sample_menu: CursesMenu, sample_items: List[MenuItem]):
    sample_menu.go_to(ord("2"))
    assert sample_menu.current_option == 1
    assert sample_menu.current_item is sample_items[1]
    sample_menu.go_to(ord("7"))
    assert sample_menu.current_option == 1
    assert sample_menu.current_item is sample_items[1]


def test_go_to_big(big_menu: CursesMenu):
    big_menu.go_to(ord("8"))
    assert big_menu.current_option == 7
    assert big_menu.current_item == big_menu.items[7]


def test_go_to_empty(empty_menu: CursesMenu):
    empty_menu.go_to(ord("1"))


def test_select(sample_menu: CursesMenu, sample_items: List[MenuItem]):
    sample_menu.select()
    assert sample_menu.current_option == 0
    assert sample_menu.current_item is sample_items[0]
    sample_menu.go_down()
    sample_menu.select()
    assert sample_menu.current_option == 1
    assert sample_menu.current_item is sample_items[1]
    sample_menu.go_down()
    sample_menu.select()
    assert sample_menu.current_option == 2
    assert type(sample_menu.current_item) == ExitItem
    sample_menu.join(timeout=10)
    assert not sample_menu.is_alive()


def test_go_to_exit(sample_menu: CursesMenu):
    sample_menu.go_to_exit()
    assert sample_menu.current_option == 2
    assert type(sample_menu.current_item) == ExitItem


def test_exit(sample_menu: CursesMenu):
    sample_menu.exit()
    sample_menu.join(timeout=10)
    assert not sample_menu.is_alive()


def test_basic_menu():
    menu = CursesMenu("Test Menu")
    menu.get_input = menu._exit
    menu.show()


def test_thread_stuff(sample_menu: CursesMenu):
    assert sample_menu.is_running()
    sample_menu.pause()
    assert not sample_menu.is_running()
    sample_menu.resume()
    assert sample_menu.is_running()


def test_append_while_running(sample_menu: CursesMenu):
    for i in range(12):
        new_item = MenuItem(f"item{i}")
        sample_menu.items.append(new_item)


def test_init():
    menu1 = CursesMenu()
    menu2 = CursesMenu("menu2", "test_init", show_exit_item=True)
    menu3 = CursesMenu(title="menu3", subtitle="test_init", show_exit_item=False)

    assert menu1.title == ""
    assert menu2.title == "menu2"
    assert menu3.title == "menu3"

    assert menu1.subtitle == ""
    assert menu2.subtitle == "test_init"
    assert menu3.subtitle == "test_init"


def test_null_screens_main_loop():
    menu = CursesMenu("menu", "empty menu", show_exit_item=False)
    CursesMenu.stdscr = None
    menu.get_input = menu._exit
    with pytest.raises(Exception):
        menu._main_loop()


def test_repr(sample_menu: CursesMenu):
    assert (
        repr(sample_menu) == f"<{sample_menu.title}: {sample_menu.subtitle}. "
        f"{len(sample_menu.items)} items>"
    )


def test_draw_item(sample_menu):
    sample_menu.draw_item(0, sample_menu.items[0], "1")
    sample_menu.draw_item(0, sample_menu.items[0], None)


def test_resize(sample_menu):
    sample_menu.on_resize()


def test_deprecated_append(sample_menu):
    with pytest.deprecated_call():
        sample_menu.append_item(MenuItem("Deprecated Append Item"))


if __name__ == "__main__":
    pytest.main()
