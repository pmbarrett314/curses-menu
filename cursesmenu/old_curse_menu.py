from enum import Enum

from cursesmenu.items import CommandItem
from cursesmenu.items import SubmenuItem

from cursesmenu import CursesMenu
from cursesmenu.items import ExitItem
from cursesmenu.items import SelectionItem
from cursesmenu.items import FunctionItem


class menuItem(Enum):
    MENU = "menu"
    COMMAND = "command"
    EXITMENU = "exitmenu"
    FUNCTION = "function"
    NUMBER = "number"


def parse_old_menu(menu_data):
    menu_title = menu_data['title']
    menu = CursesMenu(menu_title)
    for item in menu_data["options"]:
        item_type = item["type"]
        item_title = item["title"]
        if item_type == menuItem.COMMAND:
            item_command = item["command"]
            menu.add_item(CommandItem(item_title, item_command, menu))
        elif item_type == menuItem.FUNCTION:
            item_function = item["function"]
            menu.add_item(FunctionItem(item_title, item_function, menu))
        elif item_type == menuItem.EXITMENU:
            menu.add_item(ExitItem(item_title, menu))
        elif item_type == menuItem.NUMBER:
            menu.add_item(SelectionItem(item_title, menu))
        elif item_type == menuItem.MENU:
            new_menu = parse_old_menu(item)
            menu.add_item(SubmenuItem(item_title, new_menu, menu))

    return menu
