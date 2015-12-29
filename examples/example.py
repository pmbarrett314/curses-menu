from cursesmenu import *
from cursesmenu.items import *

menu = CursesMenu("Title", "Subtitle")
item1 = MenuItem("Item", menu)
function_item = FunctionItem("Fun item", menu, input, ["Enter an input"])
command_item = CommandItem("Command", menu, "echo hello")
submenu = SelectionMenu(["item1", "item2", "item3"])
submenu_item = SubmenuItem("Submenu item", menu, submenu)
menu.append_item(item1)
menu.append_item(function_item)
menu.append_item(command_item)
menu.append_item(submenu_item)
menu.show()
