import curses
import os
import platform
import threading


class CursesMenu(object):
    """
    A class that displays a menu and allows the user to select an option

    :cvar CursesMenu cls.currently_active_menu: Class variable that holds the currently active menu or None if no menu\
    is currently active (E.G. when switching between menus)
    """
    currently_active_menu = None
    stdscr = None

    def __init__(self, title=None, subtitle=None, show_exit_option=True):
        """
        :ivar str title: The title of the menu
        :ivar str subtitle: The subtitle of the menu
        :ivar bool show_exit_option: Whether this menu should show an exit item by default. Can be overridden \
        when the menu is started
        :ivar items: The list of MenuItems that the menu will display
        :vartype items: list[:class:`MenuItem<cursesmenu.items.MenuItem>`]
        :ivar CursesMenu parent: The parent of this menu
        :ivar CursesMenu previous_active_menu: the previously active menu to be restored into the class's \
        currently active menu
        :ivar int current_option: The currently highlighted menu option
        :ivar MenuItem current_item: The item corresponding to the menu option that is currently highlighted
        :ivar int selected_option: The option that the user has most recently selected
        :ivar MenuItem selected_item: The item in :attr:`items` that the user most recently selected
        :ivar returned_value: The value returned by the most recently selected item
        :ivar screen: the curses window associated with this menu
        :ivar normal: the normal text color pair for this menu
        :ivar highlight: the highlight color pair associated with this window
        """

        self.screen = None
        self.highlight = None
        self.normal = None

        self.title = title
        self.subtitle = subtitle
        self.show_exit_option = show_exit_option

        self.items = list()

        self.parent = None

        self.exit_item = ExitItem(menu=self)

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
        :rtype: MenuItem|None
        """
        if self.items:
            return self.items[self.current_option]
        else:
            return None

    @property
    def selected_item(self):
        """
        :rtype: MenuItem|None
        """
        if self.items and self.selected_option != -1:
            return self.items[self.current_option]
        else:
            return None

    def append_item(self, item):
        """
        Add an item to the end of the menu before the exit item

        :param MenuItem item: The item to be added
        """
        did_remove = self.remove_exit()
        item.menu = self
        self.items.append(item)
        if did_remove:
            self.add_exit()
        if self.screen:
            max_row, max_cols = self.screen.getmaxyx()
            if max_row < 6 + len(self.items):
                self.screen.resize(6 + len(self.items), max_cols)
            self.draw()

    def add_exit(self):
        """
        Add the exit item if necessary. Used to make sure there aren't multiple exit items

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
        Remove the exit item if necessary. Used to make sure we only remove the exit item, not something else

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
            self._main_loop(None)
        CursesMenu.currently_active_menu = None
        self.clear_screen()
        clear_terminal()
        CursesMenu.currently_active_menu = self.previous_active_menu

    def start(self, show_exit_option=None):
        """
        Start the menu in a new thread and allow the user to interact with it.
        The thread is a daemon, so :meth:`join()<cursesmenu.CursesMenu.join>` should be called if there's a possibility\
        that the main thread will exit before the menu is done

        :param bool show_exit_option: Whether the exit item should be shown, defaults to\
        the value set in the constructor
        """

        self.previous_active_menu = CursesMenu.currently_active_menu
        CursesMenu.currently_active_menu = None

        self.should_exit = False

        if show_exit_option is None:
            show_exit_option = self.show_exit_option

        if show_exit_option:
            self.add_exit()
        else:
            self.remove_exit()

        try:
            self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)
        except TypeError:
            self._main_thread = threading.Thread(target=self._wrap_start)
            self._main_thread.daemon = True

        self._main_thread.start()

    def show(self, show_exit_option=None):
        """
        Calls start and then immediately joins.

        :param bool show_exit_option: Whether the exit item should be shown, defaults to the value set \
        in the constructor
        """
        self.start(show_exit_option)
        self.join()

    def _main_loop(self, scr):
        if scr is not None:
            CursesMenu.stdscr = scr
        self.screen = curses.newpad(len(self.items) + 6, CursesMenu.stdscr.getmaxyx()[1])
        self._set_up_colors()
        curses.curs_set(0)
        CursesMenu.stdscr.refresh()
        self.draw()
        CursesMenu.currently_active_menu = self
        self._running.set()
        while self._running.wait() is not False and not self.should_exit:
            self.process_user_input()

    def draw(self):
        """
        Redraws the menu and refreshes the screen. Should be called whenever something changes that needs to be redrawn.
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

        screen_rows, screen_cols = CursesMenu.stdscr.getmaxyx()
        top_row = 0
        if 6 + len(self.items) > screen_rows:
            if screen_rows + self.current_option < 6 + len(self.items):
                top_row = self.current_option
            else:
                top_row = 6 + len(self.items) - screen_rows

        self.screen.refresh(top_row, 0, 0, 0, screen_rows - 1, screen_cols - 1)

    def is_running(self):
        """
        :return: True if the menu is started and hasn't been paused
        """
        return self._running.is_set()

    def wait_for_start(self, timeout=None):
        """
        Block until the menu is started

        :param timeout: How long to wait before timing out
        :return: False if timeout is given and operation times out, True otherwise. None before Python 2.7
        """
        return self._running.wait(timeout)

    def is_alive(self):
        """
        :return: True if the thread is still alive, False otherwise
        """
        return self._main_thread.is_alive()

    def pause(self):
        """
        Temporarily pause the menu until resume is called
        """
        self._running.clear()

    def resume(self):
        """
        Sets the currently active menu to this one and resumes it
        """
        CursesMenu.currently_active_menu = self
        self._running.set()

    def join(self, timeout=None):
        """
        Should be called at some point after :meth:`start()<cursesmenu.CursesMenu.start>` to block until the menu exits.
        :param Number timeout: How long to wait before timing out
        """
        self._main_thread.join(timeout=timeout)

    def get_input(self):
        """
        Can be overridden to change the input method.
        Called in :meth:`process_user_input()<cursesmenu.CursesMenu.process_user_input>`

        :return: the ordinal value of a single character
        :rtype: int
        """
        return CursesMenu.stdscr.getch()

    def process_user_input(self):
        """
        Gets the next single character and decides what to do with it
        """
        user_input = self.get_input()

        go_to_max = ord("9") if len(self.items) >= 9 else ord(str(len(self.items)))

        if ord('1') <= user_input <= go_to_max:
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
        Select the current item and run it
        """
        self.selected_option = self.current_option
        self.selected_item.set_up()
        self.selected_item.action()
        self.selected_item.clean_up()
        self.returned_value = self.selected_item.get_return()
        self.should_exit = self.selected_item.should_exit

        if not self.should_exit:
            self.draw()

    def exit(self):
        """
        Signal the menu to exit, then block until it's done cleaning up
        """
        self.should_exit = True
        self.join()

    def _set_up_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def clear_screen(self):
        """
        Clear the screen belonging to this menu
        """
        self.screen.clear()


class MenuItem(object):
    """
    A generic menu item
    """

    def __init__(self, text, menu=None, should_exit=False):
        """
        :ivar str text: The text shown for this menu item
        :ivar CursesMenu menu: The menu to which this item belongs
        :ivar bool should_exit: Whether the menu should exit once this item's action is done
        """
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self):
        return "%s %s" % (self.menu.title, self.text)

    def show(self, index):
        """
        How this item should be displayed in the menu. Can be overridden, but should keep the same signature.

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
        Override to carry out the main action for this item.
        """
        pass

    def clean_up(self):
        """
        Override to add any cleanup actions necessary for the item
        """
        pass

    def get_return(self):
        """
        Override to change what the item returns.
        Otherwise just returns the same value the last selected item did.
        """
        return self.menu.returned_value


class ExitItem(MenuItem):
    """
    Used to exit the current menu. Handled by :class:`cursesmenu.CursesMenu`
    """

    def __init__(self, text="Exit", menu=None):
        super(ExitItem, self).__init__(text=text, menu=menu, should_exit=True)

    def show(self, index):
        """
        This class overrides this method
        """
        if self.menu and self.menu.parent:
            self.text = "Return to %s menu" % self.menu.parent.title
        else:
            self.text = "Exit"
        return super(ExitItem, self).show(index)


def clear_terminal():
    """
    Call the platform specific function to clear the terminal: cls on windows, reset otherwise
    """
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('reset')
