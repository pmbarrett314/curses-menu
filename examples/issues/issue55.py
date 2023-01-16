from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem

menu = CursesMenu("Title", "Subtitle")
item1 = MenuItem("这是一个中文菜单项", menu)
item2 = MenuItem("这是第二个中文菜单项", menu)
menu.append_item(item1)
menu.append_item(item2)
# Create some items
menu.start()
menu.join()
