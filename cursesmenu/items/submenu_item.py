from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


class SubmenuItem(MenuItem):
    def __init__(self, name, menu, submenu, should_exit=False):
        """
        :type submenu: CursesMenu
        """
        super().__init__(name, menu, should_exit)
        self.submenu = submenu
        self.submenu.parent = self.menu

    def action(self):
        self.menu.clear_screen()
        self.submenu.show()
        CursesMenu.currently_active_menu = self.menu
        self.menu.clear_screen()
