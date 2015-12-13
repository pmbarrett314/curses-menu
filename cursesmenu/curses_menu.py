import curses
import os
import platform


class CursesMenu():
    def __init__(self, title, subtitle=None, items=list(), exit=True, parent=None):

        """
        :type parent: CursesMenu
        :param title: str
        :param subtitle:
        :param items:
        :type items: list[menu_item.MenuItem]
        :param exit:
        """
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

        self.title = title
        self.subtitle = subtitle
        self.show_exit_option = exit
        self.options = items
        self.parent = parent

        if parent is None:
            self.exit_item = ExitItem("Exit", self)
        else:
            self.exit_item = ExitItem("Return to %s menu" % parent.title, self)

        self.current_selected = 0

        self.should_exit = False

    def show(self, exit=None):
        if exit is None:
            exit = self.show_exit_option

        if exit:
            if self.options[-1] is not self.exit_item:
                self.options.append(self.exit_item)
        else:
            if self.options[-1] is self.exit_item:
                del self.options[-1]
        self.display()
        if self.options[-1] is self.exit_item:
            del self.options[-1]

    def display(self):
        self.draw()
        # Loop until return key is pressed
        while self.get_user_input() != ord('\n'):
            self.draw()

    def draw(self):
        self.screen.border(0)
        self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        if self.subtitle is not None:
            self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.options):
            if self.current_selected == index:
                textstyle = self.highlight
            else:
                textstyle = self.normal
            self.screen.addstr(5 + index, 4, "%d - %s" % (index + 1, item.name), textstyle)
        self.screen.refresh()

    def get_user_input(self):
        x = self.screen.getch()

        if ord('1') <= x <= ord(str(len(self.options) + 1)):
            self.current_selected = x - ord('0') - 1

        elif x == curses.KEY_DOWN:
            if self.current_selected < len(self.options) - 1:
                self.current_selected += 1
            else:
                self.current_selected = 0

        elif x == curses.KEY_UP:
            if self.current_selected > 0:
                self.current_selected += -1
            else:
                self.current_selected = len(self.options) - 1

        return x

    def exit(self):
        clear_terminal()
        self.should_exit = True

    def clear_screen(self):
        self.screen.clear()


class MenuItem:
    def __init__(self, name, menu=None):
        """
        :type name: str
        :type menu: curses_menu.CursesMenu
        """
        self.name = name
        self.menu = menu

    def show(self):
        pass

    def action(self):
        pass


class SubmenuItem(MenuItem):
    def __init__(self, name, submenu, menu=None):
        """
        :type submenu: CursesMenu
        """
        super(SubmenuItem, self).__init__(name, menu)
        self.submenu = submenu
        self.submenu.parent = self.menu

    def action(self):
        self.menu.clear_screen()
        self.submenu.show()
        self.menu.clear_screen()


class ExitItem(MenuItem):
    def action(self):
        self.menu.exit()


def clear_terminal():
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('reset')


def main():
    menu = CursesMenu("Test Menu", "Subtitle", [MenuItem("hello"), MenuItem("hello2")])
    menu.show()


if __name__ == "__main__":
    main()
