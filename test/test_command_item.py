import os.path
import platform
import subprocess
from unittest.mock import Mock, patch

from cursesmenu.items import CommandItem
from test_external_item import TestExternalItem


class TestCommandItem(TestExternalItem):
    def test_init(self):
        menu_item_1 = CommandItem("test1", self.menu, "exit")
        menu_item_2 = CommandItem("test2", self.menu, "ls", ["-l", "-a", "~"], True)
        menu_item_3 = CommandItem(name="test3", menu=self.menu, command="rm", arguments=["-r", "-f", "./test"],
                                  should_exit=False)
        self.assertEqual(menu_item_1.name, "test1")
        self.assertEqual(menu_item_2.name, "test2")
        self.assertEqual(menu_item_3.name, "test3")
        self.assertEqual(menu_item_1.menu, self.menu)
        self.assertEqual(menu_item_2.menu, self.menu)
        self.assertEqual(menu_item_3.menu, self.menu)
        self.assertFalse(menu_item_1.should_exit)
        self.assertTrue(menu_item_2.should_exit)
        self.assertFalse(menu_item_3.should_exit)
        self.assertEqual(menu_item_1.command, "exit")
        self.assertEqual(menu_item_2.command, "ls")
        self.assertEqual(menu_item_3.command, "rm")
        self.assertEqual(menu_item_1.arguments, [])
        self.assertEqual(menu_item_2.arguments, ["-l", "-a", "~"])
        self.assertEqual(menu_item_3.arguments, ["-r", "-f", "./test"])

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
            expected_contents = "hello \n"
        else:
            delete_item = CommandItem("Delete", self.menu, "rm test.txt")
            expected_contents = "hello\n"

        self.assertEqual(create_item.action(), 0)
        self.assertTrue(os.path.isfile("test.txt"))
        with open("test.txt", 'r') as text:
            self.assertEqual(text.read(), expected_contents)
        self.assertEqual(delete_item.action(), 0)
        self.assertFalse(os.path.isfile("test.txt"))

    @patch('cursesmenu.items.command_item.subprocess')
    def test_call(self, mock_class):
        mock_subprocess = Mock(spec=subprocess)
        command_item = CommandItem("Command item", self.menu, "ls", ["-l", "-a", "~"])
        command_item.action()
        mock_class.run.assert_called_with("ls -l -a ~", shell=True)
