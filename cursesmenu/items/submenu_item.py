from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


class SubmenuItem(MenuItem):
    """
    A menu item that opens a submenu.
    """

    def __init__(self, name, menu, submenu, should_exit=False):
        """
        :param CursesMenu submenu: The submenu to be opened when this item is selected
        """
        super().__init__(name, menu, should_exit)
        self.submenu = submenu
        self.submenu.parent = self.menu

    def action(self):
        """
        Shows the submenu
        """
        self.menu.clear_screen()
        return_value = self.submenu.show()
        CursesMenu.currently_active_menu = self.menu
        self.menu.clear_screen()
        return return_value
