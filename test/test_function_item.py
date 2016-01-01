try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from cursesmenu.items import FunctionItem
from test_external_item import TestExternalItem


def fun1():
    return 10


def fun2(x):
    return x + 2


class TestFunctionItem(TestExternalItem):
    def test_run(self):
        mock1 = MagicMock(name="fun1", return_value=5)
        mock2 = MagicMock(name="fun2", return_value=10)

        args = [1, 2, 3]
        kwargs = {"end": "\n", "sep": " "}
        item1 = FunctionItem("Fun1", self.menu, mock1)
        item2 = FunctionItem("Fun1", self.menu, mock2, args, kwargs)
        self.assertEqual(item1.action(), 5)
        self.assertEqual(item2.action(), 10)
        mock1.assert_any_call()
        mock2.assert_called_once_with(*args, **kwargs)

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
