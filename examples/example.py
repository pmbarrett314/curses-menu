from cursesmenu import *
from cursesmenu.items import *

def main():
    menu = CursesMenu("Root Menu", "Root Menu Subtitle")
    item1 = MenuItem("Item 1", menu)
    function_item = FunctionItem("Fun item", menu, input, ["Enter an input"])
    command_item = CommandItem("Command", menu, "echo hello")
    submenu = SelectionMenu(["item1", "item2", "item3"])
    submenu_item = SubmenuItem("Submenu item", menu=menu, submenu=submenu)
    submenu_2 = CursesMenu("Submenu Title", "Submenu subtitle")
    function_item_2 = FunctionItem("Fun item", submenu_2, input, ["Enter an input"])
    item2 = MenuItem("Another Item", submenu_2)
    submenu_2.append_item(function_item_2)
    submenu_2.append_item(item2)
    submenu_item_2 = SubmenuItem("Another submenu", submenu=submenu_2, menu=menu)
    menu.append_item(item1)
    menu.append_item(function_item)
    menu.append_item(command_item)
    menu.append_item(submenu_item)
    menu.append_item(submenu_item_2)
    menu.start()
    menu.join()


if __name__ == "__main__":
    main()
