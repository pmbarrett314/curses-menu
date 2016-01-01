from threading import Thread

from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


class TestSampleMenu(BaseTestCase):
    def setUp(self):
        super(TestSampleMenu, self).setUp()

        self.menu = CursesMenu("self.menu", "TestSampleMenu")
        self.item1 = MenuItem("self.item1", self.menu)
        self.item2 = MenuItem("self.item2", self.menu)
        self.menu.append_item(self.item1)
        self.menu.append_item(self.item2)
        try:
            self.menu_thread = Thread(target=self.menu.show, daemon=True)
        except TypeError:
            self.menu_thread = Thread(target=self.menu.show)
            self.menu_thread.daemon = True
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
        menu1 = CursesMenu()
        menu2 = CursesMenu("menu2", "test_init", True, None)
        menu3 = CursesMenu(title="menu3", subtitle="test_init", show_exit_option=False, parent=menu1)
        self.assertIsNone(menu1.title)
        self.assertEqual(menu2.title, "menu2")
        self.assertEqual(menu3.title, "menu3")
        self.assertIsNone(menu1.subtitle)
        self.assertEqual(menu2.subtitle, "test_init")
        self.assertEqual(menu3.subtitle, "test_init")
        self.assertTrue(menu1.show_exit_option)
        self.assertTrue(menu2.show_exit_option)
        self.assertFalse(menu3.show_exit_option)
        self.assertIsNone(menu1.parent)
        self.assertIsNone(menu2.parent)
        self.assertEqual(menu3.parent, menu1)

    def test_currently_active_menu(self):
        menu1 = CursesMenu("menu1", "test_currently_active_menu")
        menu2 = CursesMenu("menu2", "test_currently_active_menu")
        try:
            thread1 = Thread(target=menu1.show, daemon=True)
            thread2 = Thread(target=menu2.show, daemon=True)
        except TypeError:
            thread1 = Thread(target=menu1.show)
            thread1.daemon = True
            thread2 = Thread(target=menu2.show)
            thread2.daemon = True
        self.assertIsNone(CursesMenu.currently_active_menu)
        thread1.start()
        self.assertIs(CursesMenu.currently_active_menu, menu1)
        thread2.start()
        self.assertIs(CursesMenu.currently_active_menu, menu2)
