from curses_menu import CursesMenu, MenuItem
import unittest
from threading import Thread
import curses


def fun1():
    pass


def fun2():
    pass


class TestCursesMenu(unittest.TestCase):
    def setUp(self):
        self.menu = CursesMenu("Test menu 1", "Subtitle 1")
        self.item1 = MenuItem("Item1", self.menu)
        self.item2 = MenuItem("Item2", self.menu)
        self.menu.add_item(self.item1)
        self.menu.add_item(self.item2)

    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        root_menu = CursesMenu("Test menu 1", "Subtitle 1")
        root_menu.add_item(FunctionItem("Function 1", fun1, root_menu))
        root_menu.add_item(CommandItem("Command 1", "echo 1 >> testoutput.txt", root_menu))

        submenu = CursesMenu("Test menu 2", "Subtitle 2", parent=root_menu)
        submenu.add_item(FunctionItem("Fun2", fun2, submenu))
        root_menu.add_item(SubmenuItem("Submenu 1", submenu, root_menu))

        cls.menu = root_menu
        """

    def test_init(self):
        Thread(target=self.menu.show, daemon=True).start()
        self.assertEqual(self.menu.current_option, 0)
        self.assertEqual(self.menu.current_item, self.item1)

    def test_go_down(self):
        Thread(target=self.menu.show, daemon=True).start()
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 1)
        self.assertIs(self.menu.current_item, self.item2)
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 2)
        self.assertEqual(self.menu.current_item, self.menu.exit_item)
        self.menu.go_down()
        self.assertEqual(self.menu.current_option, 0)
        self.assertIs(self.menu.current_item, self.item1)

    def test_go_up(self):
        Thread(target=self.menu.show, daemon=True).start()
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 2)
        self.assertIs(self.menu.current_item, self.menu.exit_item)
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 1)
        self.assertEqual(self.menu.current_item, self.item2)
        self.menu.go_up()
        self.assertEqual(self.menu.current_option, 0)
        self.assertIs(self.menu.current_item, self.item1)


if __name__ == "__main__":
    log_file = 'unittests.txt'
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
        f.close()
