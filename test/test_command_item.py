import unittest
from cursesmenu.command_item import CommandItem
import platform


class TestCommandItem(unittest.TestCase):
    def setUp(self):
        CommandItem.set_up_terminal = lambda _: None
        CommandItem.clean_up_terminal = lambda _: None
        if platform.system().lower() == "windows":
            self.item1 = CommandItem("Bad Command", "del", None)
        else:
            self.item1 = CommandItem("Bad Command", "return 1", None)

    def test_run(self):
        self.assertEqual(self.item1.action(), 1)
