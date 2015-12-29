from threading import Thread
from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem
from base_test_case import BaseTestCase


class TestCursesMenu(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.menu = CursesMenu("Test menu 1", "Subtitle 1")
        self.item1 = MenuItem("Item1", self.menu)
        self.item2 = MenuItem("Item2", self.menu)
        self.menu.append_item(self.item1)
        self.menu.append_item(self.item2)
        self.menu_thread = Thread(target=self.menu.show, daemon=True)
        self.menu_thread.start()

    def test_init(self):
        self.assertEqual(self.menu.current_option, 0)
        self.assertEqual(self.menu.current_item, self.item1)

    def test_go_down(self):
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 1)
        self.assertIs(self.menu.current_item, self.item2)
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 2)
        self.assertEqual(self.menu.current_item, self.menu.exit_item)
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 0)
        self.assertIs(self.menu.current_item, self.item1)

    def test_go_up(self):
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 2)
        self.assertIs(self.menu.current_item, self.menu.exit_item)
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 1)
        self.assertEqual(self.menu.current_item, self.item2)
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 0)
        self.assertIs(self.menu.current_item, self.item1)

    def test_select(self):
        self.menu.select()
        self.assertEqual(self.menu.selected_option, 0)
        self.assertIs(self.menu.selected_item, self.item1)
        self.menu.go_down()
        self.menu.select()
        self.assertEqual(self.menu.selected_option, 1)
        self.assertIs(self.menu.selected_item, self.item2)
        self.menu.go_down()
        self.menu.select()
        self.assertEqual(self.menu.selected_option, 2)
        self.assertIs(self.menu.selected_item, self.menu.exit_item)
        self.menu_thread.join(timeout=5)
        self.assertFalse(self.menu_thread.is_alive())

    def test_exit(self):
        self.menu.exit()
        self.menu_thread.join(timeout=5)
        self.assertFalse(self.menu_thread.is_alive())
