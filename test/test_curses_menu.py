from threading import Thread

from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


class TestSampleMenu(BaseTestCase):
    def setUp(self):
        super(TestSampleMenu, self).setUp()

        self.menu = CursesMenu("Test menu 1", "Subtitle 1")
        self.item1 = MenuItem("Item1", self.menu)
        self.item2 = MenuItem("Item2", self.menu)
        self.menu.append_item(self.item1)
        self.menu.append_item(self.item2)
        self.menu_thread = Thread(target=self.menu.show, daemon=True)
        self.menu_thread.start()

    def tearDown(self):
        super(TestSampleMenu, self).tearDown()
        self.menu.exit()
        self.menu_thread.join()

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

    def test_go_to(self):
        self.menu.go_to(1)
        self.assertEqual(self.menu.current_option, 1)
        self.assertEqual(self.menu.current_item, self.item2)

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


class TestCursesMenu(BaseTestCase):
    def test_init(self):
        menu_1 = CursesMenu()
        menu_2 = CursesMenu("title", "subtitle", True, None)
        menu_3 = CursesMenu(title="title2", subtitle="subtitle2", show_exit_option=False, parent=menu_1)
        self.assertIsNone(menu_1.title)
        self.assertEqual(menu_2.title, "title")
        self.assertEqual(menu_3.title, "title2")
        self.assertIsNone(menu_1.subtitle)
        self.assertEqual(menu_2.subtitle, "subtitle")
        self.assertEqual(menu_3.subtitle, "subtitle2")
        self.assertTrue(menu_1.show_exit_option)
        self.assertTrue(menu_2.show_exit_option)
        self.assertFalse(menu_3.show_exit_option)
        self.assertIsNone(menu_1.parent)
        self.assertIsNone(menu_2.parent)
        self.assertEqual(menu_3.parent, menu_1)
