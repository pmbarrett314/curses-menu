from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import SelectionItem


class TestSelectionItem(BaseTestCase):
    def setUp(self):
        super(TestSelectionItem, self).setUp()
        self.menu = CursesMenu("self.menu", "TestSelectionItem")

    def test_init(self):
        selection_item_1 = SelectionItem("selection_item_1", 1, self.menu)
        selection_item_2 = SelectionItem(text="selection_item_2", index=2, menu=self.menu)
        self.assertEqual(selection_item_1.text, "selection_item_1")
        self.assertEqual(selection_item_2.text, "selection_item_2")
        self.assertEqual(selection_item_1.menu, self.menu)
        self.assertEqual(selection_item_2.menu, self.menu)
        self.assertTrue(selection_item_1.should_exit)
        self.assertTrue(selection_item_2.should_exit)
