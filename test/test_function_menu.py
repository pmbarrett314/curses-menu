from base_test_case import BaseTestCase
from cursesmenu.function_item import FunctionItem


def fun1():
    return 10


def fun2(x):
    return x + 2


class TestCommandItem(BaseTestCase):
    def setUp(self):
        super().setUp()
        FunctionItem.set_up_terminal = lambda _: None
        FunctionItem.clean_up_terminal = lambda _: None
        self.item1 = FunctionItem("Function 1", fun1, None)
        self.item2 = FunctionItem("Function 2", fun2, None, 2)

    def test_run(self):
        self.assertEqual(self.item1.action(), 10)
        self.assertEqual(self.item2.action(), 4)
