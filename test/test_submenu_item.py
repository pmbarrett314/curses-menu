import unittest
from cursesmenu.submenu_item import SubmenuItem
import cursesmenu.curses_menu
from cursesmenu.curses_menu import CursesMenu, MenuItem
from threading import Thread


class TestSubmenuItem(unittest.TestCase):
    def setUp(self):
        CursesMenu.set_up_screen = lambda _: None
        CursesMenu.clear_screen = lambda _: None
        CursesMenu.draw = lambda _: None
        CursesMenu.set_up_colors = lambda _: None
        cursesmenu.curses_menu.clean_up_screen = lambda: None
        cursesmenu.curses_menu.clear_terminal = lambda: None
        self.menu = CursesMenu("Test menu 1", "Subtitle 1")
        self.menu.get_input = lambda: ord('a')
        self.submenu1 = CursesMenu("Test submenu 1", "Subtitle 2")
        self.submenu1.get_input = lambda: ord('a')
        self.item1 = SubmenuItem("Item1", self.submenu1, self.menu)
        self.submenu1_thread = Thread(target=self.item1.action, daemon=True)
        self.submenu2 = CursesMenu("Test submenu 2", "Subtitle 3")
        self.submenu2.get_input = lambda: ord('a')
        self.item2 = SubmenuItem("Item2", self.submenu2, self.menu)
        self.submenu2_thread = Thread(target=self.item2.action, daemon=True)
        self.menu.add_item(self.item1)
        self.menu.add_item(self.item2)
        self.menu_thread = Thread(target=self.menu.show, daemon=True)
        self.menu_thread.start()

    def test_action(self):
        self.submenu1_thread.start()
        self.assertIs(CursesMenu.currently_active_menu, self.submenu1)
        CursesMenu.currently_active_menu.exit()
        self.submenu1_thread.join(timeout=10)
        self.assertIs(CursesMenu.currently_active_menu, self.menu)
        self.submenu2_thread.start()
        self.assertIs(CursesMenu.currently_active_menu, self.submenu2)
