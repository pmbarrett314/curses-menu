from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import ExitItem


class TestExitItem(BaseTestCase):
    def test_init(self):
        menu = CursesMenu("menu", "test_init")
        exit_item_1 = ExitItem("exit_item_1", menu)
        exit_item_2 = ExitItem(name="exit_item_2", menu=menu)
        self.assertEqual(exit_item_1.name, "exit_item_1")
        self.assertEqual(exit_item_2.name, "exit_item_2")
        self.assertEqual(exit_item_1.menu, menu)
        self.assertEqual(exit_item_2.menu, menu)
        self.assertTrue(exit_item_1.should_exit)
        self.assertTrue(exit_item_2.should_exit)
