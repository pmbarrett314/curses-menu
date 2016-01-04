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
        super(SubmenuItem, self).__init__(name, menu, should_exit)
        self.submenu = submenu
        self.submenu.parent = self.menu

    def set_up(self):
        """
        Pause the parent menu and clear the screen
        :return:
        """
        self.menu.pause()
        self.menu.clear_screen()

    def action(self):
        """
        Shows the submenu
        """
        self.submenu.show()

    def clean_up(self):
        """
        Wait on the submenu to return, then clean up and resume the parent menu
        """
        self.submenu.join()
        self.submenu.clear_screen()
        self.menu.resume()
