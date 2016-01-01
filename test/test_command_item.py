import os.path
import platform

from cursesmenu import CursesMenu

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from cursesmenu.items import CommandItem
from test_external_item import TestExternalItem


class TestCommandItem(TestExternalItem):
    def setUp(self):
        super(TestCommandItem, self).setUp()
        self.menu = CursesMenu("self.menu", "TestCommnadItem")

    def test_init(self):
        command_item_1 = CommandItem("command_item_1", self.menu, "exit")
        command_item_2 = CommandItem("command_item_2", self.menu, "ls", ["-l", "-a", "~"], True)
        command_item_3 = CommandItem(name="command_item_3", menu=self.menu, command="rm",
                                     arguments=["-r", "-f", "./test"],
                                     should_exit=False)
        self.assertEqual(command_item_1.name, "command_item_1")
        self.assertEqual(command_item_2.name, "command_item_2")
        self.assertEqual(command_item_3.name, "command_item_3")
        self.assertEqual(command_item_1.menu, self.menu)
        self.assertEqual(command_item_2.menu, self.menu)
        self.assertEqual(command_item_3.menu, self.menu)
        self.assertFalse(command_item_1.should_exit)
        self.assertTrue(command_item_2.should_exit)
        self.assertFalse(command_item_3.should_exit)
        self.assertEqual(command_item_1.command, "exit")
        self.assertEqual(command_item_2.command, "ls")
        self.assertEqual(command_item_3.command, "rm")
        self.assertEqual(command_item_1.arguments, [])
        self.assertEqual(command_item_2.arguments, ["-l", "-a", "~"])
        self.assertEqual(command_item_3.arguments, ["-r", "-f", "./test"])

    def test_return(self):
        if platform.system().lower() == "windows":
            return_command_item = CommandItem("return_command_item", self.menu, "exit 1")
        else:
            return_command_item = CommandItem("return_command_item", self.menu, "return 1")
        self.assertEqual(return_command_item.action(), 1)

    def test_run(self):
        create_item = CommandItem("create_item", self.menu, 'echo hello>test.txt')
        if platform.system().lower() == "windows":
            delete_item = CommandItem("delete_item", self.menu, "del test.txt")
            expected_contents = "hello \n"
        else:
            delete_item = CommandItem("delete_item", self.menu, "rm test.txt")
            expected_contents = "hello\n"

        self.assertEqual(create_item.action(), 0)
        self.assertTrue(os.path.isfile("test.txt"))
        with open("test.txt", 'r') as text:
            self.assertEqual(text.read(), expected_contents)
        self.assertEqual(delete_item.action(), 0)
        self.assertFalse(os.path.isfile("test.txt"))

    @patch('cursesmenu.items.command_item.subprocess')
    def test_call(self, mock_class):
        command_item = CommandItem("command_item", self.menu, "ls", ["-l", "-a", "~"])
        command_item.action()
        mock_class.run.assert_called_with("ls -l -a ~", shell=True)
