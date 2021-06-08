"""A base class for menu items that need to exit the menu environment temporarily."""

import curses

import cursesmenu.curses_menu
import cursesmenu.utils
from cursesmenu.curses_menu import MenuItem


class ExternalItem(MenuItem):
    """A base class for menu items that need to exit the menu environment\
     temporarily."""

    def set_up(self) -> None:
        """Return the console to its original state and pauses the menu."""
        assert self.menu is not None

        self.menu.pause()
        curses.def_prog_mode()
        cursesmenu.utils.clear_terminal()
        self.menu.clear_screen()

    def clean_up(self) -> None:
        """Put the console back in curses mode and resumes the menu."""
        assert self.menu is not None

        self.menu.clear_screen()
        curses.reset_prog_mode()
        curses.curs_set(1)  # reset doesn't do this right
        curses.curs_set(0)
        self.menu.resume()
