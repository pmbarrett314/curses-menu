from enum import Enum
from typing import Any, Dict

from cursesmenu import CursesMenu
from cursesmenu.curses_menu import _SelectionItem
from cursesmenu.items import CommandItem, ExitItem, FunctionItem, SubmenuItem


class menuItem(Enum):
    MENU = "menu"
    COMMAND = "command"
    EXITMENU = "exitmenu"
    FUNCTION = "function"
    NUMBER = "number"


def parse_old_menu(menu_data: Dict[str, Any]) -> CursesMenu:
    """
    Take an old-style menuData dictionary and return a CursesMenu

    :param dict menu_data:
    :return: A new CursesMenu
    :rtype: CursesMenu
    """
    menu_title = menu_data["title"]
    menu = CursesMenu(menu_title)
    for index, item in enumerate(menu_data["options"]):
        item_type = item["type"]
        item_title = item["title"]
        if item_type == menuItem.COMMAND:
            item_command = item["command"]
            menu.append_item(CommandItem(item_title, item_command, menu=menu))
        elif item_type == menuItem.FUNCTION:
            item_function = item["function"]
            menu.append_item(FunctionItem(item_title, item_function, menu=menu))
        elif item_type == menuItem.EXITMENU:
            menu.append_item(ExitItem(menu=menu))
        elif item_type == menuItem.NUMBER:
            menu.append_item(_SelectionItem(text=item_title, index=index, menu=menu))
        elif item_type == menuItem.MENU:
            new_menu = parse_old_menu(item)
            menu.append_item(SubmenuItem(item_title, menu, new_menu))

    return menu
