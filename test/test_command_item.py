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
        self.menu = CursesMenu("self.menu", "TestCommandItem")

    def test_init(self):
        command_item_1 = CommandItem("command_item_1", "exit")
        command_item_2 = CommandItem("command_item_2", "ls", ["-l", "-a", "~"], self.menu, True)
        command_item_3 = CommandItem(text="command_item_3", command="rm", menu=self.menu,
                                     arguments=["-r", "-f", "./test"], should_exit=False)

        self.assertEqual(command_item_1.text, "command_item_1")
        self.assertEqual(command_item_2.text, "command_item_2")
        self.assertEqual(command_item_3.text, "command_item_3")
        self.assertEqual(command_item_1.menu, None)
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
            return_command_item = CommandItem("return_command_item", "exit 1")
        else:
            return_command_item = CommandItem("return_command_item", "return 1")

        return_command_item.action()

        self.assertEqual(return_command_item.get_return(), 1)

    def test_run(self):
        create_item = CommandItem("create_item", 'echo hello>test.txt')
        if platform.system().lower() == "windows":
            delete_item = CommandItem("delete_item", "del test.txt")
            expected_contents = "hello \n"
        else:
            delete_item = CommandItem("delete_item", "rm test.txt")
            expected_contents = "hello\n"
        create_item.action()
        self.assertEqual(create_item.get_return(), 0)
        self.assertTrue(os.path.isfile("test.txt"))

        with open("test.txt", 'r') as text:
            self.assertEqual(text.read(), expected_contents)

        delete_item.action()
        self.assertEqual(delete_item.get_return(), 0)
        self.assertFalse(os.path.isfile("test.txt"))

    @patch('cursesmenu.items.command_item.subprocess')
    def test_call(self, mock_class):
        command_item = CommandItem("command_item", "ls", ["-l", "-a", "~"])
        command_item.action()
        mock_class.run.assert_called_with("ls -l -a ~", shell=True)
