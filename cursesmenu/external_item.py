from cursesmenu.curses_menu import MenuItem
from cursesmenu.curses_menu import clear_terminal, reset_prog_mode
import curses


class ExternalItem(MenuItem):
    def set_up_terminal(self):
        curses.def_prog_mode()
        clear_terminal()
        self.menu.clear_screen()

    def action(self):
        self.set_up_terminal()
        return_value = self.external_action()
        self.clean_up_terminal()
        return return_value

    def clean_up_terminal(self):
        self.menu.clear_screen()
        reset_prog_mode()

    def external_action(self):
        pass
