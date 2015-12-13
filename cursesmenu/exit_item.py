from curses_menu import MenuItem


class ExitItem(MenuItem):
    def selected(self):
        self.menu.exit()
