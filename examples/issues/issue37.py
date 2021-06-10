from cursesmenu import *
from cursesmenu.items import *

menu = CursesMenu("Title", "Subtitle")
selection_menu = CursesMenu.make_selection_menu(["item{}".format(i) for i in range(20)])
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)
menu.append_item(submenu_item)
menu.show()
