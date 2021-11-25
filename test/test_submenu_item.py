import pytest

from cursesmenu import CursesMenu
from cursesmenu.items import SubmenuItem

pytestmark = pytest.mark.usefixtures(
    "mock_cursesmenu_curses",
    "mock_clear",
)


def test_submenu():
    root_menu = CursesMenu("root_menu", "test_action")
    submenu1 = CursesMenu("submenu1", "test_action")
    submenu2 = CursesMenu("submenu2", "test_action")

    submenu2.returned_value = 1

    submenu_item_1 = SubmenuItem("submenu_item_1", submenu1, menu=root_menu)
    submenu_item_2 = SubmenuItem("submenu_item_2", submenu2, menu=root_menu)
    root_menu.items.append(submenu_item_1)
    root_menu.items.append(submenu_item_2)

    assert submenu1.end_items[0].show("q") == "q - Return to root_menu menu"

    root_menu.start()
    root_menu.wait_for_start(timeout=10)
    assert root_menu.is_alive()
    assert root_menu.is_running()
    assert not submenu1.is_alive()
    assert not submenu1.is_running()
    submenu_item_1.set_up()
    submenu_item_1.action()
    submenu1.wait_for_start(timeout=10)
    assert root_menu.is_alive()
    assert not root_menu.is_running()
    assert submenu1.is_alive()
    assert submenu1.is_running()
    submenu1.exit()
    submenu_item_1.clean_up()
    root_menu.returned_value = submenu_item_1.get_return()
    assert root_menu.returned_value is None
    assert root_menu.is_alive()
    assert root_menu.is_running()
    assert not submenu1.is_alive()
    assert not submenu1.is_running()
    submenu_item_2.set_up()
    submenu_item_2.action()
    submenu2.wait_for_start(timeout=10)
    assert root_menu.is_alive()
    assert not root_menu.is_running()
    assert submenu2.is_alive()
    assert submenu2.is_running()
    submenu2.exit()
    submenu_item_2.clean_up()
    root_menu.returned_value = submenu_item_2.get_return()
    assert root_menu.returned_value == 1
    assert root_menu.is_alive()
    assert root_menu.is_running()
    assert not submenu1.is_alive()
    assert not submenu1.is_running()
    assert not submenu2.is_alive()
    assert not submenu2.is_running()
    root_menu.exit()
    assert not root_menu.is_alive()
    assert not root_menu.is_running()
    assert not submenu1.is_alive()
    assert not submenu1.is_running()
    assert not submenu2.is_alive()
    assert not submenu2.is_running()


def test_null_submenu():
    root_menu = CursesMenu("root_menu", "test_action")
    submenu1 = CursesMenu("submenu1", "test_action")
    submenu2 = CursesMenu("submenu2", "test_action")

    submenu2.returned_value = 1

    submenu_item_1 = SubmenuItem("submenu_item_1", submenu1, menu=root_menu)
    submenu_item_2 = SubmenuItem("submenu_item_2", menu=root_menu)
    submenu_item_2.submenu = submenu2
    root_menu.items.append(submenu_item_1)
    root_menu.items.append(submenu_item_2)

    submenu_item_1.submenu = None
    assert submenu_item_1.get_return() is None
