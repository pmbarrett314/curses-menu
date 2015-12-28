import platform

from cursesmenu.items import CommandItem
from test_external_item import TestExternalItem


class TestCommandItem(TestExternalItem):
    def setUp(self):
        super().setUp()
        if platform.system().lower() == "windows":
            self.item1 = CommandItem("Bad Command", "del", self.menu)
        else:
            self.item1 = CommandItem("Bad Command", "return 1", self.menu)

    def test_run(self):
        self.assertEqual(self.item1.action(), 1)
