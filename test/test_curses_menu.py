from curses_menu import CursesMenu
from function_item import FunctionItem
from submenu_item import SubmenuItem


def fun1():
    pass


def fun2():
    pass


def main():
    root_menu = CursesMenu("Test menu 1", "Subtitle 1")
    root_menu.add_item(FunctionItem("Function 1", fun1, root_menu))

    submenu = CursesMenu("Test menu 2", "Subtitle 2", parent=root_menu)
    submenu.add_item(FunctionItem("Fun2", fun2, submenu))
    root_menu.add_item(SubmenuItem("Submenu 1", submenu, root_menu))

    root_menu.show()


if __name__ == "__main__":
    main()
