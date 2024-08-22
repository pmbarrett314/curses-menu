from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem

menu = CursesMenu("Title", "Subtitle")
item1 = MenuItem("这是一个中文菜单项", menu)
item2 = MenuItem("这是第二个中文菜单项", menu)
menu.items.append(item1)
menu.items.append(item2)
# Create some items
menu.start()
menu.join()
