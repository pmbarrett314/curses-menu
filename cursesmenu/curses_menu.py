import curses
import os
import platform

import exit_item


class CursesMenu():
    def __init__(self, title, subtitle=None, items=list(), exit=True, parent=None):

        """
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

        self.exit_item = exit_item.ExitItem("Exit", self)

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

    def display(self):
        oldpos = None  # used to prevent the s lf.screen being redrawn every time
        x = None  # control for while loop, let's you scroll through options until return key is pressed then returns pos to program


        self.draw()
        # Loop until return key is pressed
        while self.get_user_input() != ord('\n'):
            if self.current_selected != oldpos:
                oldpos = self.current_selected
                self.draw()


        # return index of the selected item
        return self.current_selected

    def draw(self):
        self.screen.border(0)
        self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)  # Title for this menuData
        if self.subtitle is not None:
            self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)  # Subtitle for this menuData

        # Display all the menuData items, showing the 'pos' item highlighted
        for index in range(len(self.options)):
            textstyle = self.normal
            if self.current_selected == index:
                textstyle = self.highlight
            self.screen.addstr(5 + index, 4, "%d - %s" % (index + 1, self.options[index].name), textstyle)
        self.screen.refresh()
        # finished updating self.screen

    def get_user_input(self):
        x = self.screen.getch()  # Gets user input

        # What is user input?
        if ord('1') <= x <= ord(str(len(self.options) + 1)):
            self.current_selected = x - ord('0') - 1  # convert keypress back to a number, then subtract 1 to get index
        elif x == 258:  # down arrow
            if self.current_selected < len(self.options) - 1:
                self.current_selected += 1
            else:
                self.current_selected = 0
        elif x == 259:  # up arrow
            if self.current_selected > 0:
                self.current_selected += -1
            else:
                self.current_selected = len(self.options) - 1
        return x

    def exit(self):
        clear_terminal()
        self.should_exit = True


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
