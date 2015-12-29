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
