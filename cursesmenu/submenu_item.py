from cursesmenu.curses_menu import MenuItem, CursesMenu


class SubmenuItem(MenuItem):
    def __init__(self, name, submenu, menu):
        """
        :type submenu: CursesMenu
        """
        super(SubmenuItem, self).__init__(name, menu)
        self.submenu = submenu
        self.submenu.parent = self.menu

    def action(self):
        self.menu.clear_screen()
        self.submenu.show()
        CursesMenu.currently_active_menu = self.menu
        self.menu.clear_screen()
