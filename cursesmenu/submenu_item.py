from curses_menu import MenuItem, CursesMenu


class SubmenuItem(MenuItem):
    def __init__(self, name, submenu, menu=None):
        """
        :type submenu: CursesMenu
        """
        super(SubmenuItem, self).__init__(name, menu)
        self.submenu = submenu
        self.submenu.parent = self.menu

    def action(self):
        self.menu.clear_screen()
        self.submenu.show()
        self.menu.clear_screen()
