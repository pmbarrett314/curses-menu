import platform
import os.path
from cursesmenu.items import CommandItem
from test_external_item import TestExternalItem
from unittest.mock import Mock, patch
import subprocess


class TestCommandItem(TestExternalItem):
    def test_return(self):
        if platform.system().lower() == "windows":
            command_item = CommandItem("Bad Command", self.menu, "exit 1")
        else:
            command_item = CommandItem("Bad Command", self.menu, "return 1")
        self.assertEqual(command_item.action(), 1)

    def test_run(self):
        create_item = CommandItem("Create", self.menu, 'echo hello>test.txt')
        if platform.system().lower() == "windows":
            delete_item = CommandItem("Delete", self.menu, "del test.txt")
        else:
            delete_item = CommandItem("Delete", self.menu, "rm test.txt")

        self.assertEqual(create_item.action(), 0)
        self.assertTrue(os.path.isfile("test.txt"))
        with open("test.txt", 'r') as text:
            self.assertEqual(text.read(), "hello \n")
        self.assertEqual(delete_item.action(), 0)

    @patch('cursesmenu.items.command_item.subprocess')
    def test_call(self, mock_class):
        mock_subprocess = Mock(spec=subprocess)
        command_item = CommandItem("Command item", self.menu, "ls", ["-l", "-a", "~"])
        command_item.action()
        mock_class.run.assert_called_with("ls -l -a ~", shell=True)
