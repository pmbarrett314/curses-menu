import curses

import cursesmenu.curses_menu
from cursesmenu.curses_menu import MenuItem


class ExternalItem(MenuItem):
    """
    A base class for items that need to do stuff on the console outside of curses mode.
    Sets the terminal back to standard mode until the action is done.
    Should probably be subclassed.
    """

    def set_up(self):
        """
        This class overrides this method
        """
        self.menu.pause()
        curses.def_prog_mode()
        cursesmenu.curses_menu.clear_terminal()
        self.menu.clear_screen()

    def clean_up(self):
        """
        This class overrides this method
        """
        self.menu.clear_screen()
        curses.reset_prog_mode()
        curses.curs_set(1)  # reset doesn't do this right
        curses.curs_set(0)
        self.menu.resume()
