from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


class TestMenuItem(BaseTestCase):
    def setUp(self):
        super(TestMenuItem, self).setUp()
        self.menu = CursesMenu("self.menu", "TestMenuItem")

    def test_init(self):
        menu_item_1 = MenuItem("menu_item_1", self.menu)
        menu_item_2 = MenuItem("menu_item_2", self.menu, True)
        menu_item_3 = MenuItem(text="menu_item_1", menu=self.menu, should_exit=False)
        self.assertEqual(menu_item_1.text, "menu_item_1")
        self.assertEqual(menu_item_2.text, "menu_item_2")
        self.assertEqual(menu_item_3.text, "menu_item_1")
        self.assertEqual(menu_item_1.menu, self.menu)
        self.assertEqual(menu_item_2.menu, self.menu)
        self.assertEqual(menu_item_3.menu, self.menu)
        self.assertFalse(menu_item_1.should_exit)
        self.assertTrue(menu_item_2.should_exit)
        self.assertFalse(menu_item_3.should_exit)

    def test_show(self):
        menu_item = MenuItem("menu_item", self.menu)
        self.assertEqual(menu_item.show(0), "1 - menu_item")
