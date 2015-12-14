from curses_menu import MenuItem
from curses_menu import clear_terminal, reset_prog_mode
import curses


class ExternalItem(MenuItem):
    def action(self):
        curses.def_prog_mode()
        clear_terminal()
        self.menu.clear_screen()
        return_value = self.external_action()
        self.menu.clear_screen()
        reset_prog_mode()
        return return_value

    def external_action(self):
        pass
