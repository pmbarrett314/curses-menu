from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import SelectionItem


class TestExitItem(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.menu = CursesMenu("Test menu 1", "Subtitle 1")

    def test_init(self):
        menu_item_1 = SelectionItem("test1", self.menu)
        menu_item_3 = SelectionItem(name="test2", menu=self.menu)
        self.assertEqual(menu_item_1.name, "test1")
        self.assertEqual(menu_item_3.name, "test2")
        self.assertEqual(menu_item_1.menu, self.menu)
        self.assertEqual(menu_item_3.menu, self.menu)
        self.assertTrue(menu_item_1.should_exit)
        self.assertTrue(menu_item_3.should_exit)
