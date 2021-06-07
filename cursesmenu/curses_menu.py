import curses
import os
import sys
import threading

MIN_SIZE = 6  # Top bar, space, title, space, subtitle, space, bottom bar


class CursesMenu(object):
    """
    A class that displays a menu and allows the user to select an option

    :cvar CursesMenu cls.currently_active_menu: Class variable that holds the \
    currently active menu or None if no menu\
    is currently active (E.G. when switching between menus)
    """

    currently_active_menu = None
    stdscr = None

    def __init__(self, title="", subtitle="", show_exit_item=True):
        """
        :ivar str title: The title of the menu
        :ivar str subtitle: The subtitle of the menu
        :ivar bool show_exit_item: Whether this menu should show an exit \
        item by default. Can be overridden when the menu is started
        :ivar items: The list of MenuItems that the menu will display
        :vartype items: list[:class:`MenuItem<cursesmenu.items.MenuItem>`]
        :ivar CursesMenu parent: The parent of this menu
        :ivar CursesMenu previous_active_menu: the previously active menu to be \
        restored into the class's currently active menu
        :ivar int current_option: The currently highlighted menu option
        :ivar MenuItem current_item: The item corresponding to the menu option \
        that is currently highlighted
        :ivar int selected_option: The option that the user has most recently selected
        :ivar MenuItem selected_item: The item in :attr:`items` that the user most \
        recently selected
        :ivar returned_value: The value returned by the most recently selected item
        :ivar screen: the curses window associated with this menu
        :ivar normal: the normal text color pair for this menu
        :ivar highlight: the highlight color pair associated with this window
        """

        self.title = title
        self.subtitle = subtitle

        self.screen = None

        self.highlight = None
        self.normal = None

        self.items = []

        self.exit_item = ExitItem(menu=self)
        self.show_exit_item = show_exit_item

        self.current_option = 0
        self.selected_option = -1

        self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)

        self._running = threading.Event()

        self.should_exit = False

        self.returned_value = None

        self.parent = None

        self.previous_active_menu = None

    def __repr__(self):
        return "%s: %s. %d items" % (self.title, self.subtitle, len(self.items))

    @classmethod
    def make_selection_menu(
        cls,
        selections,
        title,
        subtitle,
        show_exit_item=False,
    ):
        """
        Create a menu from a list of strings.

        The return value of the menu will be an index into the list of strings.

        :param selections: A list of strings to be selected from
        :param title: The title of the menu
        :param subtitle: The subtitle of the menu
        :param show_exit_item: If the exit item should be shown.\
        If it is  and the user selects it, the return value will be None
        :return: A CursesMenu with items for each selection
        """
        menu = cls(title=title, subtitle=subtitle, show_exit_item=show_exit_item)
        for index, selection in enumerate(selections):
            menu.append_item(
                _SelectionItem(text=selection, index=index, should_exit=True),
            )
        return menu

    @classmethod
    def get_selection(
        cls,
        selections,
        title,
        subtitle,
    ):
        """
        Present the user with a menu built from a list of strings and get the index\
        of their selection.

        :param selections: The list of string possibilities
        :param title: The title of the menu
        :param subtitle: The subtitle of the menu
        :return: The index in the list of strings that the user selected
        """
        menu = cls.make_selection_menu(
            selections=selections,
            title=title,
            subtitle=subtitle,
            show_exit_item=False,
        )
        menu.show()
        return menu.returned_value

    @property
    def current_item(self):
        """
        :rtype: MenuItem|None
        """
        if self.current_option == len(self.items) and self.show_exit_item:
            return self.exit_item
        elif self.items:
            return self.items[self.current_option]
        else:
            return None

    @property
    def selected_item(self):
        """
        :rtype: MenuItem|None
        """
        if self.selected_option == -1:
            return None
        elif self.selected_option == len(self.items) and self.show_exit_item:
            return self.exit_item
        else:
            return self.items[self.selected_option]

    @property
    def menu_height(self) -> int:
        return len(self.items) + MIN_SIZE + (1 if self.show_exit_item else 0)

    @property
    def last_item_index(self) -> int:
        return len(self.items) if self.show_exit_item else len(self.items) - 1

    def show(self, show_exit_item=None):
        """
        Calls start and then immediately joins.

        :param bool show_exit_item: Whether the exit item should be shown, \
        defaults to the value set in the constructor
        """
        self.start(show_exit_item)
        self.join()

    def start(self, show_exit_item=None):
        """
        Start the menu in a new thread and allow the user to interact with it.
        The thread is a daemon, so :meth:`join()<cursesmenu.CursesMenu.join>` \
        should be called if there's a possibility that the main thread will \
        exit before the menu is done

        :param bool show_exit_item: Whether the exit item should be shown, \
        defaults to the value set in the constructor
        """

        self.previous_active_menu = CursesMenu.currently_active_menu
        CursesMenu.currently_active_menu = None

        self._main_thread.start()

    def _wrap_start(self):
        if self.parent is None:
            curses.wrapper(self._main_loop)
        else:
            self._main_loop(None)
        CursesMenu.currently_active_menu = None
        self.clear_screen()
        clear_terminal()
        CursesMenu.currently_active_menu = self.previous_active_menu

    def _main_loop(self, scr):
        if scr is not None:
            CursesMenu.stdscr = scr
        self.screen = curses.newpad(self.menu_height, CursesMenu.stdscr.getmaxyx()[1])
        self._set_up_colors()
        curses.curs_set(0)
        CursesMenu.stdscr.refresh()
        self.draw()
        CursesMenu.currently_active_menu = self
        self._running.set()
        while self._running.wait() is not False and not self.should_exit:
            self.process_user_input()
        self._running.clear()

    def _set_up_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def draw(self):
        """
        Redraws the menu and refreshes the screen. Should be called whenever \
        something changes that needs to be redrawn.
        """

        self.screen.border(0)
        self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.items):
            self.draw_item(index, item)
        if self.show_exit_item:
            self.draw_item(len(self.items), self.exit_item, "q")

        self.refresh_screen()

    def draw_item(self, index, item, index_text=None):
        if index_text is None:
            index_text = str(index + 1)
        text_style = self.highlight if self.current_option == index else self.normal
        assert self.screen is not None and text_style is not None

        self.screen.addstr(
            MIN_SIZE - 1 + index,
            4,
            item.show(index_text),
            text_style,
        )

    def refresh_screen(self) -> None:
        assert CursesMenu.stdscr is not None
        screen_rows, screen_cols = CursesMenu.stdscr.getmaxyx()

        if self.menu_height > screen_rows:
            top_row = min(self.menu_height - screen_rows, self.current_option)
        else:
            top_row = 0

        self.screen.refresh(top_row, 0, 0, 0, screen_rows - 1, screen_cols - 1)

    def process_user_input(self):
        """
        Gets the next single character and decides what to do with it
        """
        user_input = self.get_input()

        if user_input is None:
            return user_input

        go_to_max = ord("9") if len(self.items) >= 9 else ord(str(len(self.items)))

        if ord("1") <= user_input <= go_to_max:
            self.go_to(user_input)
        elif user_input == curses.KEY_DOWN:
            self.go_down()
        elif user_input == curses.KEY_UP:
            self.go_up()
        elif user_input == ord("\n"):
            self.select()

        return user_input

    def get_input(self):
        """
        Can be overridden to change the input method.
        Called in :meth:`process_user_input()<cursesmenu.CursesMenu.process_user_input>`

        :return: the ordinal value of a single character
        :rtype: int
        """
        return CursesMenu.stdscr.getch()

    def select(self):
        """
        Select the current item and run it
        """
        if not self.items:
            self.should_exit = True
            return
        self.selected_option = self.current_option
        self.selected_item.set_up()
        self.selected_item.action()
        self.selected_item.clean_up()
        self.returned_value = self.selected_item.get_return()
        self.should_exit = self.selected_item.should_exit

        if not self.should_exit:
            self.draw()

    def _exit(self):
        self.should_exit = True

    def go_to(self, user_input):
        """
        Go to the option entered by the user as a number

        :param option: the option to go to
        :type option: int
        """
        if len(self.items) > 9:
            go_to_max = ord("9")
        elif len(self.items) < 0:
            return
        else:
            go_to_max = ord(str(len(self.items)))

        if ord("1") <= user_input <= go_to_max:
            self.current_option = user_input - ord("0") - 1
            self.draw()

    def go_to_exit(self):
        if self.show_exit_item:
            self.current_option = len(self.items)
            self.draw()

    def go_down(self):
        """
        Go down one, wrap to beginning if necessary
        """
        if self.current_option < self.last_item_index:
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
            self.current_option = self.last_item_index
        self.draw()

    def clear_screen(self):
        """
        Clear the screen belonging to this menu
        """
        self.screen.clear()

    def join(self, timeout=None):
        """
        Should be called at some point after \
        :meth:`start()<cursesmenu.CursesMenu.start>` to block until the menu exits.
        :param Number timeout: How long to wait before timing out
        """
        self._main_thread.join(timeout=timeout)

    def is_running(self):
        """
        :return: True if the menu is started and hasn't been paused
        """
        return self._running.is_set()

    def wait_for_start(self, timeout=None):
        """
        Block until the menu is started

        :param timeout: How long to wait before timing out
        :return: False if timeout is given and operation times out, \
        True otherwise. None before Python 2.7
        """
        return self._running.wait(timeout)

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

    def is_alive(self):
        """
        :return: True if the thread is still alive, False otherwise
        """
        return self._main_thread.is_alive()

    def exit(self):
        """
        Signal the menu to exit, then block until it's done cleaning up
        """
        self.should_exit = True
        self.join()

    def append_item(self, item):
        """
        Add an item to the end of the menu before the exit item

        :param MenuItem item: The item to be added
        """
        item.menu = self
        self.items.append(item)

        if self.screen:
            max_row, max_cols = self.screen.getmaxyx()
            if max_row < MIN_SIZE + len(self.items):
                self.screen.resize(self.menu_height, max_cols)
            self.draw()


class MenuItem(object):
    """
    A generic menu item
    """

    def __init__(self, text, menu=None, should_exit=False):
        """
        :ivar str text: The text shown for this menu item
        :ivar CursesMenu menu: The menu to which this item belongs
        :ivar bool should_exit: Whether the menu should exit once this \
        item's action is done
        """
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self):
        title = self.menu.title if self.menu else ""
        return "%s %s" % (title, self.text)

    def show(self, index):
        """
        How this item should be displayed in the menu. Can be overridden, \
        but should keep the same signature.

        Default is:

            1 - Item 1

            2 - Another Item

        :param int index: The index of the item in the items list of the menu
        :return: The representation of the item to be shown in a menu
        :rtype: str
        """
        return "%s - %s" % (index, self.text)

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
        if self.menu:
            return self.menu.returned_value
        return None


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


class _SelectionItem(MenuItem):
    def __init__(
        self,
        text,
        index,
        should_exit=False,
        menu=None,
    ):
        super(_SelectionItem, self).__init__(
            text=text,
            should_exit=should_exit,
            menu=menu,
        )
        self.index = index

    def get_return(self):
        return self.index


def clear_terminal() -> None:
    """
    Call the platform specific function to clear the terminal.

    Cls on windows, reset otherwise.
    """
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("reset")
