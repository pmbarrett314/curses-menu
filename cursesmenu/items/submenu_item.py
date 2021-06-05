import curses

from cursesmenu.curses_menu import MenuItem


class SubmenuItem(MenuItem):
    """
    A menu item to open a submenu
    """

    def __init__(self, text, submenu=None, menu=None, should_exit=False):
        """
        :ivar CursesMenu self.submenu: The submenu to be opened when \
        this item is selected
        """
        self._submenu = submenu
        self._menu = menu
        if self._submenu:
            self._submenu.parent = menu
        super(SubmenuItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

    @property
    def submenu(self):
        return self._submenu

    @submenu.setter
    def submenu(self, submenu):
        self._submenu = submenu
        if self._submenu is not None:
            self._submenu.parent = self._menu

    @property
    def menu(self):
        return self._menu

    @menu.setter
    def menu(self, menu):
        self._menu = menu
        if self._submenu is not None:
            self._submenu.parent = menu

    def set_up(self):
        """
        This class overrides this method
        """
        self.menu.pause()
        curses.def_prog_mode()
        self.menu.clear_screen()

    def action(self):
        """
        This class overrides this method
        """
        self.submenu.start()

    def clean_up(self):
        """
        This class overrides this method
        """
        self.submenu.join()
        self.menu.clear_screen()
        curses.reset_prog_mode()
        curses.curs_set(1)  # reset doesn't do this right
        curses.curs_set(0)
        self.menu.resume()

    def get_return(self):
        """
        :return: The returned value in the submenu
        """
        if self.submenu:
            return self.submenu.returned_value
        return None
