from threading import Thread

from base_test_case import BaseTestCase, ThreadedReturnGetter
from cursesmenu import CursesMenu
from cursesmenu import SelectionMenu


class TestSelectionMenu(BaseTestCase):
    def test_select(self):
        selection_menu = SelectionMenu(strings=["a", "b", "c"], title="Select a letter")

        menu_thread = Thread(target=selection_menu.show, daemon=True)
        menu_thread.start()
        selection_menu.go_down()
        selection_menu.select()
        menu_thread.join(timeout=5)
        self.assertEqual(selection_menu.selected_option, 1)

    def test_get_selection(self):
        self.menu_thread = ThreadedReturnGetter(SelectionMenu.get_selection, ["One", "Two", "Three"])
        self.menu_thread.start()
        CursesMenu.currently_active_menu.go_down()
        CursesMenu.currently_active_menu.select()
        self.menu_thread.join(timeout=5)
        self.assertEqual(self.menu_thread.return_value, 1)

    def test_init(self):
        selection_menu_1 = SelectionMenu(["1", "2", "3"])
        selection_menu_2 = SelectionMenu(["4", "5"], "Title", "subtitle", True, None)
        selection_menu_3 = SelectionMenu(strings=["6", "7", "8", "9"], title="Title 2", subtitle="subtitle 2",
                                         show_exit_option=False, parent=None)
        self.assertIsNone(selection_menu_1.title)
        self.assertEqual(selection_menu_2.title, "Title")
        self.assertEqual(selection_menu_3.title, "Title 2")
        self.assertIsNone(selection_menu_1.subtitle)
        self.assertEqual(selection_menu_2.subtitle, "subtitle")
        self.assertEqual(selection_menu_3.subtitle, "subtitle 2")
        self.assertTrue(selection_menu_1.show_exit_option)
        self.assertTrue(selection_menu_2.show_exit_option)
        self.assertFalse(selection_menu_3.show_exit_option)
        self.assertIsNone(selection_menu_1.parent)
        self.assertIsNone(selection_menu_2.parent)
        self.assertIsNone(selection_menu_3.parent)
        self.assertEqual(selection_menu_1.items[1].name, "2")
        self.assertEqual(selection_menu_2.items[0].name, "4")
        self.assertEqual(selection_menu_3.items[3].name, "9")
