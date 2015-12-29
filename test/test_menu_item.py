from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


class TestMenuItem(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.menu = CursesMenu("Test menu 1", "Subtitle 1")

    def test_init(self):
        menu_item_1 = MenuItem("test1", self.menu)
        menu_item_2 = MenuItem("test2", self.menu, True)
        menu_item_3 = MenuItem(name="test3", menu=self.menu, should_exit=False)
        self.assertEqual(menu_item_1.name, "test1")
        self.assertEqual(menu_item_2.name, "test2")
        self.assertEqual(menu_item_3.name, "test3")
        self.assertEqual(menu_item_1.menu, self.menu)
        self.assertEqual(menu_item_2.menu, self.menu)
        self.assertEqual(menu_item_3.menu, self.menu)
        self.assertFalse(menu_item_1.should_exit)
        self.assertTrue(menu_item_2.should_exit)
        self.assertFalse(menu_item_3.should_exit)

    def test_show(self):
        menu_item = MenuItem("test", self.menu)
        self.assertEqual(menu_item.show(0), "1 - test")
