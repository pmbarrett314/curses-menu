import platform

from cursesmenu.items import CommandItem
from test_external_item import TestExternalItem


class TestCommandItem(TestExternalItem):
    def setUp(self):
        super().setUp()
        if platform.system().lower() == "windows":
            self.item1 = CommandItem("Bad Command", self.menu, "del")
        else:
            self.item1 = CommandItem("Bad Command", self.menu, "return 1")

    def test_run(self):
        self.assertEqual(self.item1.action(), 1)
