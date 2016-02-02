import curses
import os
import platform
import threading


class CursesMenu(object):
    """
    A class that displays a menu and allows the user to select an option

    :cvar cls.currently_active_menu: The currently active menu
    :type currently_active_menu: CursesMenu
    """
    currently_active_menu = None

    def __init__(self, title=None, subtitle=None, show_exit_option=True):
        """
        :type title: str
        :type subtitle: str
        :type show_exit_option: bool

        :ivar str self.title: The title of the menu
        :ivar str self.subtitle: The subtitle of the menu
        :ivar self.items: The list of MenuItems that the menu will display
        :vartype self.items: list[MenuItem]
        :ivar bool self.show_exit_option: Whether this menu should show an exit item by default. can be overridden in :meth:`CursesMenu.show`
        :ivar CursesMenu self.parent: The parent of this menu
        :ivar int self.current_option: The currently highlighted menu option
        :ivar MenuItem self.current_item: The item corresponding to the menu option that is currently highlighted
        :ivar int self.selected_option: The option that the user has most recently selected
        :ivar MenuItem self.selected_item: The item in :attr:`self.items` that the user most recently selected
        :ivar self.returned_value: The value returned by the most recently selected item
        :type self._main_thread: threading.Thread
        :type self._running: threading.Event

        """

        self.screen = None
        self.highlight = None
        self.normal = None

        self.title = title
        self.subtitle = subtitle
        self.show_exit_option = show_exit_option

        self.items = list()

        self.parent = None

        self.exit_item = ExitItem("Exit", self)

        self.current_option = 0
        self.selected_option = -1

        self.returned_value = None

        self.should_exit = False

        self.previous_active_menu = None

        self._main_thread = None

        self._running = threading.Event()

    def __repr__(self):
        return "%s: %s. %d items" % (self.title, self.subtitle, len(self.items))

    @property
    def current_item(self):
        """
        :rtype: MenuItem or None
        """
        if self.items:
            return self.items[self.current_option]
        else:
            return

    @property
    def selected_item(self):
        """
        :rtype: MenuItem or None
        """
        if self.items and self.selected_option != -1:
            return self.items[self.current_option]
        else:
            return None

    def set_parent(self, menu):
        self.parent = menu
        self.exit_item = ExitItem("Return to %s menu" % self.parent.title, self)

    def append_item(self, item):
        """
        Append an item to the menu

        :param item: The item to be added
        :type item: MenuItem
        """
        did_remove = self.remove_exit()
        item.menu = self
        self.items.append(item)
        if did_remove:
            self.add_exit()

    def add_exit(self):
        """
        Add the exit item if necessary

        :return: True if item needed to be added, False otherwise
        :rtype: bool
        """
        if self.items:
            if self.items[-1] is not self.exit_item:
                self.items.append(self.exit_item)
                return True
        return False

    def remove_exit(self):
        """
        Remove the exit item if necessary

        :return: True if item needed to be removed, False otherwise
        :rtype: bool
        """
        if self.items:
            if self.items[-1] is self.exit_item:
                del self.items[-1]
                return True
        return False

    def _wrap_start(self):
        if self.parent is None:
            curses.wrapper(self._main_loop)
        else:
            self._main_loop(curses.initscr())

    def start(self, exit_option=None):
        """
        Start the menu and allow the user to interact with it

        :param exit_option: Whether the exit item should be shown, defaults to the value set in the constructor
        :type exit_option: bool
        """

        self.previous_active_menu = CursesMenu.currently_active_menu
        CursesMenu.currently_active_menu = None

        self.should_exit = False

        if exit_option is None:
            exit_option = self.show_exit_option

        if exit_option:
            self.add_exit()
        else:
            self.remove_exit()

        try:
            self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)
        except TypeError:
            self._main_thread = threading.Thread(target=self._wrap_start)
            self._main_thread.daemon = True

        self._main_thread.start()

    def show(self, exit_option=None):
        self.start(exit_option)
        self.join()

    def _main_loop(self, scr):
        self.screen = scr
        self._set_up_colors()
        self.draw()
        CursesMenu.currently_active_menu = self
        self._running.set()
        while self._running.wait() is not False and not self.should_exit:
            self.process_user_input()

    def draw(self):
        """
        Redraws the menu and refreshes the screen. Should be called whenever something changes.
        """
        self.screen.border(0)
        if self.title is not None:
            self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        if self.subtitle is not None:
            self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.items):
            if self.current_option == index:
                text_style = self.highlight
            else:
                text_style = self.normal
            self.screen.addstr(5 + index, 4, item.show(index), text_style)
        self.screen.refresh()

    def is_running(self):
        return self._running.is_set()

    def wait_for_start(self, timeout=None):
        self._running.wait(timeout)

    def is_alive(self):
        """
        :return: True if the thread is still alive, False otherwise
        """
        return self._main_thread.is_alive()

    def pause(self):
        """
        Temporarily pause this menu until resume is called
        """
        self._running.clear()

    def resume(self):
        """
        Sets the currently active menu to this one and resumes ut
        """
        CursesMenu.currently_active_menu = self
        self._running.set()

    def join(self, timeout=None):
        """
        Wait on the menu to exit then return
        :param Number timeout: How long to wait before timing out
        """
        if threading.current_thread() is not self._main_thread:
            self._main_thread.join(timeout=timeout)

    def get_input(self):
        """
        Can be overridden to change the input method
        Called in process_user_input

        :return: a single character at a time
        :rtype: int
        """
        return self.screen.getch()

    def process_user_input(self):
        """
        Gets user input and decides what to do with it
        Called in show.
        """
        user_input = self.get_input()

        if ord('1') <= user_input <= ord(str(len(self.items) + 1)):
            self.go_to(user_input - ord('0') - 1)
        elif user_input == curses.KEY_DOWN:
            self.go_down()
        elif user_input == curses.KEY_UP:
            self.go_up()
        elif user_input == ord("\n"):
            self.select()

        return user_input

    def go_to(self, option):
        """
        Go to the option entered by the user as a number

        :param option: the option to go to
        :type option: int
        """
        self.current_option = option
        self.draw()

    def go_down(self):
        """
        Go down one, wrap to beginning if necessary
        """
        if self.current_option < len(self.items) - 1:
            self.current_option += 1
        else:
            self.current_option = 0
        self.draw()

    def go_up(self):
        """
        Go up one, wrap to end if necessary
        """
        if self.current_option > 0:
            self.current_option += -1
        else:
            self.current_option = len(self.items) - 1
        self.draw()

    def select(self):
        """
        Select the current item and run its action() method
        """
        self.selected_option = self.current_option
        self.selected_item.set_up()
        self.returned_value = self.selected_item.action()
        self.selected_item.clean_up()

        if self.selected_item.should_exit:
            self.exit()
        else:
            self.draw()

    def exit(self):
        """
        Exit the menu and clean up
        :return: The return value of the most recently selected item
        """
        clear_terminal()
        self.should_exit = True
        CursesMenu.currently_active_menu = None
        self.join()
        clean_up_screen()
        self.clear_screen()
        CursesMenu.currently_active_menu = self.previous_active_menu
        return self.returned_value

    def _set_up_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def clear_screen(self):
        self.screen.clear()


class MenuItem(object):
    """
    A generic menu item
    """

    def __init__(self, text, menu=None, should_exit=False):
        """
        :type text: str
        :type menu: CursesMenu

        :ivar str self.name: The name shown for this menu item
        :ivar CursesMenu self.menu: The menu to which this item belongs
        :ivar bool self.should_exit: whether the menu should exit once this item's action is done
        """
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self):
        return "%s %s" % (self.menu.title, self.text)

    def show(self, index):
        """
        How this item should be displayed in the menu. Can be overridden as desired as long as it returns a string
        and takes an int as its first parameter.

        Default is:

            1 - Item 1
            2 - Another Item

        :param int index: The index of the item in the items list of the menu
        :return: The representation of the item to be shown in a menu
        :rtype: str
        """
        return "%d - %s" % (index + 1, self.text)

    def set_up(self):
        """
        Override to add any setup actions necessary for the item
        """
        pass

    def action(self):
        """
        What should be done when this item is selected. Should be overridden as needed.
        """
        pass

    def clean_up(self):
        """
        Override to add any cleanup actions necessary for the item
        """
        pass


class ExitItem(MenuItem):
    """
    The last item in the menu, used to exit the current menu.
    """

    def __init__(self, text, menu=None):
        super(ExitItem, self).__init__(text=text, menu=menu, should_exit=True)


def clear_terminal():
    """
    Call the platform specific function to clear the terminal: cls on windows, reset otherwise
    """
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('reset')


def clean_up_screen():
    """
    Final cleanup after the menu is finished
    """
    curses.endwin()
    clear_terminal()


def reset_prog_mode():
    """
    Restore the terminal mode
    """
    curses.reset_prog_mode()  # reset to 'current' curses environment
    curses.curs_set(1)  # reset doesn't do this right
    curses.curs_set(0)
