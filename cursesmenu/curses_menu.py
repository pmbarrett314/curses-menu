import curses
import os
import platform


class CursesMenu():
    def __init__(self, title, subtitle=None, items=None, exit_option=True, parent=None):
        """
        :param title: the title of the menu
        :type title: str
        :param subtitle: the subtitle of the menu
        :type subtitle: str
        :param items:
        :param exit_option:
        :param parent:
        :return:
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
        self.show_exit_option = exit_option
        if items is None:
            self.items = list()
        else:
            self.items = items
        self.parent = parent

        if parent is None:
            self.exit_item = ExitItem("Exit", self)
        else:
            self.exit_item = ExitItem("Return to %s menu" % parent.title, self)

        self.current_option = 0
        self.current_item = None
        self.selected_option = -1
        self.selected_item = None

        self.should_exit = False

    def add_item(self, item):
        self.remove_exit()
        self.items.append(item)

    def add_exit(self):
        if self.items:
            if self.items[-1] is not self.exit_item:
                self.items.append(self.exit_item)

    def remove_exit(self):
        if self.items:
            if self.items[-1] is self.exit_item:
                del self.items[-1]

    def show(self, exit_option=None):
        if exit_option is None:
            exit_option = self.show_exit_option

        if exit_option:
            self.add_exit()
        else:
            self.remove_exit()

        if self.current_item is None and self.items:
            self.current_item = self.items[0]

        return_value = None
        while self.selected_item is not self.exit_item and not self.should_exit:
            return_value = self.display()

        self.remove_exit()

        curses.endwin()
        clear_terminal()
        return return_value

    def display(self):
        self.draw()
        while self.get_user_input() != ord('\n'):
            self.draw()
        self.selected_option = self.current_option
        self.selected_item = self.items[self.selected_option]
        return self.selected_item.action()

    def draw(self):
        self.screen.border(0)
        self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        if self.subtitle is not None:
            self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.items):
            if self.current_option == index:
                textstyle = self.highlight
            else:
                textstyle = self.normal
            self.screen.addstr(5 + index, 4, "%d - %s" % (index + 1, item.name), textstyle)
        self.screen.refresh()

    def get_user_input(self):
        x = self.screen.getch()

        if ord('1') <= x <= ord(str(len(self.items) + 1)):
            self.current_option = x - ord('0') - 1

        elif x == curses.KEY_DOWN:
            if self.current_option < len(self.items) - 1:
                self.current_option += 1
            else:
                self.current_option = 0

        elif x == curses.KEY_UP:
            if self.current_option > 0:
                self.current_option += -1
            else:
                self.current_option = len(self.items) - 1
        self.current_item = self.items[self.current_option]

        return x

    def exit(self):
        clear_terminal()
        self.should_exit = True

    def clear_screen(self):
        self.screen.clear()


class MenuItem:
    def __init__(self, name, menu):
        """
        :type name: str
        :type menu: curses_menu.CursesMenu
        """
        self.name = name
        self.menu = menu

    def __str__(self):
        return "%s %s" % (self.menu.title, self.name)

    def show(self):
        pass

    def action(self):
        pass


class ExitItem(MenuItem):
    def action(self):
        self.menu.exit()


def clear_terminal():
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('reset')


def reset_prog_mode():
    curses.reset_prog_mode()  # reset to 'current' curses environment
    curses.curs_set(1)  # reset doesn't do this right
    curses.curs_set(0)


def main():
    menu = CursesMenu("Test Menu", "Subtitle", [MenuItem("hello"), MenuItem("hello2")])
    menu.show()


if __name__ == "__main__":
    main()
