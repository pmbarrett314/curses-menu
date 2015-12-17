import unittest
from cursesmenu.command_item import CommandItem


class TestCommandItem(unittest.TestCase):
    def setUp(self):
        CommandItem.set_up_terminal = lambda _: None
        CommandItem.clean_up_terminal = lambda _: None
        self.item1 = CommandItem("Bad Command", "del", None)

    def test_run(self):
        self.assertEqual(self.item1.action(), 1)
