import curses

from cursesmenu import clear_terminal
from cursesmenu.items import MenuItem


class ExternalItem(MenuItem):
    """
    A base class for items that need to do stuff on the console.
    Takes care of changing the terminal mode back and forth.
    """

    def set_up(self):
        self.menu.pause()
        curses.def_prog_mode()
        clear_terminal()
        self.menu.clear_screen()

    def clean_up(self):
        self.menu.clear_screen()
        curses.reset_prog_mode()
        self.menu.resume()
