from base_test_case import BaseTestCase

from cursesmenu import CursesMenu
from cursesmenu.items import ExitItem


class TestExitItem(BaseTestCase):
    def test_init(self):
        menu = CursesMenu("menu", "test_init")
        exit_item_1 = ExitItem("exit_item_1")
        exit_item_2 = ExitItem("exit_item_2", menu)
        exit_item_3 = ExitItem(text="exit_item_3", menu=menu)
        self.assertEqual(exit_item_1.text, "exit_item_1")
        self.assertEqual(exit_item_2.text, "exit_item_2")
        self.assertEqual(exit_item_3.text, "exit_item_3")
        self.assertEqual(exit_item_1.menu, None)
        self.assertEqual(exit_item_2.menu, menu)
        self.assertEqual(exit_item_3.menu, menu)
        self.assertTrue(exit_item_1.should_exit)
        self.assertTrue(exit_item_2.should_exit)
        self.assertTrue(exit_item_3.should_exit)
