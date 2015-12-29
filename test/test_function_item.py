from cursesmenu.items import FunctionItem
from test_external_item import TestExternalItem


def fun1():
    return 10


def fun2(x):
    return x + 2


class TestFunctionItem(TestExternalItem):
    def setUp(self):
        super().setUp()
        self.item1 = FunctionItem("Function 1", self.menu, fun1)
        self.item2 = FunctionItem("Function 2", self.menu, fun2, [2])

    def test_run(self):
        self.assertEqual(self.item1.action(), 10)
        self.assertEqual(self.item2.action(), 4)

    def test_init(self):
        menu_item_1 = FunctionItem("test1", self.menu, fun1)
        menu_item_2 = FunctionItem("test2", self.menu, fun1, ["-l", "-a", "~"], {"test": 12}, True)
        menu_item_3 = FunctionItem(name="test3", menu=self.menu, function=fun2, args=[1, 2, 3],
                                   kwargs={1: "thing", 16: "other"}, should_exit=False)
        self.assertEqual(menu_item_1.name, "test1")
        self.assertEqual(menu_item_2.name, "test2")
        self.assertEqual(menu_item_3.name, "test3")
        self.assertEqual(menu_item_1.menu, self.menu)
        self.assertEqual(menu_item_2.menu, self.menu)
        self.assertEqual(menu_item_3.menu, self.menu)
        self.assertFalse(menu_item_1.should_exit)
        self.assertTrue(menu_item_2.should_exit)
        self.assertFalse(menu_item_3.should_exit)
        self.assertEqual(menu_item_1.function, fun1)
        self.assertEqual(menu_item_2.function, fun1)
        self.assertEqual(menu_item_3.function, fun2)
        self.assertEqual(menu_item_1.args, [])
        self.assertEqual(menu_item_2.args, ["-l", "-a", "~"])
        self.assertEqual(menu_item_3.args, [1, 2, 3])
        self.assertEqual(menu_item_1.kwargs, {})
        self.assertEqual(menu_item_2.kwargs, {"test": 12})
        self.assertEqual(menu_item_3.kwargs, {1: "thing", 16: "other"})
