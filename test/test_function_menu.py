import unittest
from cursesmenu.function_item import FunctionItem


def fun1():
    return 10


class TestCommandItem(unittest.TestCase):
    def setUp(self):
        FunctionItem.set_up_terminal = lambda _: None
        FunctionItem.clean_up_terminal = lambda _: None
        self.item1 = FunctionItem("Function", fun1, None)

    def test_run(self):
        self.assertEqual(self.item1.action(), 10)
