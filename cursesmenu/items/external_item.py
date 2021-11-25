"""A base class for menu items that need to exit the menu environment temporarily."""

import curses

import cursesmenu.utils
from cursesmenu.items.menu_item import MenuItem


class ExternalItem(MenuItem):
    """A base class for menu items that need to exit the menu environment\
     temporarily."""

    def set_up(self) -> None:
        """Return the console to its original state and pause the menu."""
        assert self.menu is not None
        curses.def_prog_mode()
        self.menu.clear_screen()
        self.menu.pause()
        curses.endwin()
        cursesmenu.utils.soft_clear_terminal()

    def clean_up(self) -> None:
        """Put the console back in curses mode and resume the menu."""
        assert self.menu is not None
        curses.reset_prog_mode()
        self.menu.resume()
