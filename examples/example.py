from cursesmenu import CursesMenu
from cursesmenu.items import CommandItem, FunctionItem, MenuItem, SubmenuItem


def main():
    menu = CursesMenu("Root Menu", "Root Menu Subtitle")
    item1 = MenuItem("Basic item that does nothing", menu)
    function_item = FunctionItem("FunctionItem, get input", input, ["Enter an input: "])
    print(__file__)
    command_item = CommandItem(
        "CommandItem that opens another menu",
        f"python {__file__}",
    )

    submenu = CursesMenu.make_selection_menu([f"item{x}" for x in range(1, 20)])
    submenu_item = SubmenuItem("Long Selection SubMenu", submenu=submenu, menu=menu)

    submenu_2 = CursesMenu("Submenu Title", "Submenu subtitle")
    function_item_2 = FunctionItem("Fun item", input, ["Enter an input"])
    item2 = MenuItem("Another Item")
    submenu_2.items.append(function_item_2)
    submenu_2.items.append(item2)
    submenu_item_2 = SubmenuItem("Short Submenu", submenu=submenu_2, menu=menu)

    menu.items.append(item1)
    menu.items.append(function_item)
    menu.items.append(command_item)
    menu.items.append(submenu_item)
    menu.items.append(submenu_item_2)

    menu.start()
    _ = menu.join()


if __name__ == "__main__":
    main()
