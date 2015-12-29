import curses

from cursesmenu import clear_terminal, reset_prog_mode
from cursesmenu.items import MenuItem


class ExternalItem(MenuItem):
    """
    A base class for items that need to do stuff on the console.
    Takes care of changing the terminal mode back and forth.
    """

    def _set_up_terminal(self):
        curses.def_prog_mode()
        clear_terminal()
        self.menu.clear_screen()

    def action(self):
        """
        Does all the setup and cleanup necessary for the terminal and calls external_action
        :return: the value returned from the external action
        """
        self._set_up_terminal()
        return_value = self.external_action()
        self._clean_up_terminal()
        return return_value

    def _clean_up_terminal(self):
        self.menu.clear_screen()
        reset_prog_mode()

    def external_action(self):
        """
        Override to do whatever should be done in the terminal when this item is selected
        """
        pass
