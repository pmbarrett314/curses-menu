import curses
import os
import sys
import threading
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, DefaultDict, List, Optional, cast

if TYPE_CHECKING:
    # noinspection PyCompatibility,PyProtectedMember
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    Window = Any
    MenuItem = Any

MIN_SIZE = 6  # Top bar, space, title, space, subtitle, space, bottom bar


class CursesMenu(object):
    """
    A class that displays a menu and allows the user to select an option

    :cvar CursesMenu cls.currently_active_menu: Class variable that holds the \
    currently active menu or None if no menu\
    is currently active (E.G. when switching between menus)
    """

    currently_active_menu = None
    stdscr: Optional[Window] = None

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        show_exit_item: bool = True,
    ):
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

        self.screen: Optional[Window] = None

        self.highlight: Optional[int] = None
        self.normal: Optional[int] = None

        self.items: List[MenuItem] = []

        self.exit_item = ExitItem(menu=self)
        self.show_exit_item = show_exit_item

        self.current_option = 0
        self.selected_option = -1

        self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)

        self._running = threading.Event()

        self.should_exit = False

        self.returned_value = None

        self.parent: Optional[CursesMenu] = None

        self.user_input_handlers: DefaultDict[int, Callable[[int], None]] = defaultdict(
            null_input_factory,
        )
        self.user_input_handlers.update(
            {
                ord("\n"): self.select,
                curses.KEY_UP: self.go_up,
                curses.KEY_DOWN: self.go_down,
                ord("q"): self.go_to_exit,
            },
        )
        self.user_input_handlers.update(
            {k: self.go_to for k in map(ord, map(str, range(1, 10)))},
        )
        self.previous_active_menu = None

    def __repr__(self) -> str:
        return f"{self.title}: {self.subtitle}. {len(self.items)} items"

    @classmethod
    def make_selection_menu(
        cls,
        selections: List[str],
        title: str,
        subtitle: str,
        show_exit_item: bool = False,
    ) -> "CursesMenu":
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
        selections: List[str],
        title: str,
        subtitle: str,
    ) -> int:
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
        return cast(int, menu.show())

    @property
    def current_item(self) -> Optional[MenuItem]:
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
    def selected_item(self) -> Optional[MenuItem]:
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

    def show(self) -> Any:
        """
        Calls start and then immediately joins.

        :param bool show_exit_item: Whether the exit item should be shown, \
        defaults to the value set in the constructor
        """
        self.start()
        return self.join()

    def start(self) -> None:
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

    def _wrap_start(self) -> None:
        if self.parent is None:
            curses.wrapper(self._main_loop)
        else:
            self._main_loop(None)
        CursesMenu.currently_active_menu = None
        self.clear_screen()
        clear_terminal()
        CursesMenu.currently_active_menu = self.previous_active_menu

    def _main_loop(self, scr: Optional[Window]) -> None:
        if scr is not None:
            CursesMenu.stdscr = scr
        if CursesMenu.stdscr is None:
            raise Exception("main loop entered without a root screen")
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

    def _set_up_colors(self) -> None:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def draw(self) -> None:
        """
        Redraws the menu and refreshes the screen. Should be called whenever \
        something changes that needs to be redrawn.
        """
        assert self.screen is not None
        self.screen.border(0)
        self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.items):
            self.draw_item(index, item)
        if self.show_exit_item:
            self.draw_item(len(self.items), self.exit_item, "q")

        self.refresh_screen()

    def draw_item(
        self,
        index: int,
        item: MenuItem,
        index_text: Optional[str] = None,
    ) -> None:
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
        assert self.screen is not None
        screen_rows, screen_cols = CursesMenu.stdscr.getmaxyx()

        if self.menu_height > screen_rows:
            top_row = min(self.menu_height - screen_rows, self.current_option)
        else:
            top_row = 0

        self.screen.refresh(top_row, 0, 0, 0, screen_rows - 1, screen_cols - 1)

    def process_user_input(self) -> int:
        """
        Gets the next single character and decides what to do with it
        """
        user_input = self.get_input()
        self.user_input_handlers[user_input](user_input)
        return user_input

    # noinspection PyMethodMayBeStatic
    def get_input(self) -> int:
        """
        Can be overridden to change the input method.
        Called in :meth:`process_user_input()<cursesmenu.CursesMenu.process_user_input>`

        :return: the ordinal value of a single character
        :rtype: int
        """
        assert CursesMenu.stdscr is not None
        return CursesMenu.stdscr.getch()

    def select(self, _: int = 0) -> None:
        """
        Select the current item and run it
        """
        if not self.items:
            self._exit()
            return
        self.selected_option = self.current_option

        assert self.selected_item is not None
        self.selected_item.set_up()
        self.selected_item.action()
        self.selected_item.clean_up()
        self.returned_value = self.selected_item.get_return()
        self.should_exit = self.selected_item.should_exit

        if not self.should_exit:
            self.draw()

    def _exit(self) -> None:
        self.should_exit = True

    def go_to(self, user_input: int) -> None:
        """
        Go to the option entered by the user as a number

        :param option: the option to go to
        :type option: int
        """
        if self.last_item_index > 9:
            go_to_max = ord("9")
        elif self.last_item_index < 0:
            return
        else:
            go_to_max = ord(str(self.last_item_index))
        # TODO: Make this use a buffer for multi-digit numbers
        # TODO: also use for letters
        if ord("1") <= user_input <= go_to_max:
            self.current_option = user_input - ord("0") - 1
            self.draw()

    def go_to_exit(self, _: int = 0) -> None:
        if self.show_exit_item:
            self.current_option = len(self.items)
            self.draw()

    def go_down(self, _: int = 0) -> None:
        """
        Go down one, wrap to beginning if necessary
        """
        if self.current_option < self.last_item_index:
            self.current_option += 1
        else:
            self.current_option = 0
        self.draw()

    def go_up(self, _: int = 0) -> None:
        """
        Go up one, wrap to end if necessary
        """
        if self.current_option > 0:
            self.current_option += -1
        else:
            self.current_option = self.last_item_index
        self.draw()

    def clear_screen(self) -> None:
        """
        Clear the screen belonging to this menu
        """
        assert self.screen is not None
        self.screen.clear()

    def join(self, timeout: Optional[int] = None) -> Any:
        """
        Should be called at some point after \
        :meth:`start()<cursesmenu.CursesMenu.start>` to block until the menu exits.
        :param Number timeout: How long to wait before timing out
        """
        self._main_thread.join(timeout=timeout)
        return self.returned_value

    def is_running(self) -> bool:
        """
        :return: True if the menu is started and hasn't been paused
        """
        return self._running.is_set()

    def wait_for_start(self, timeout: Optional[int] = None) -> bool:
        """
        Block until the menu is started

        :param timeout: How long to wait before timing out
        :return: False if timeout is given and operation times out, \
        True otherwise. None before Python 2.7
        """
        return self._running.wait(timeout)

    def pause(self) -> None:
        """
        Temporarily pause the menu until resume is called
        """
        self._running.clear()

    def resume(self) -> None:
        """
        Sets the currently active menu to this one and resumes it
        """
        CursesMenu.currently_active_menu = self
        self._running.set()

    def is_alive(self) -> bool:
        """
        :return: True if the thread is still alive, False otherwise
        """
        return self._main_thread.is_alive()

    def exit(self, timeout: Optional[int] = None) -> Any:
        """
        Signal the menu to exit, then block until it's done cleaning up
        """
        self._exit()
        return self.join(timeout)

    def append_item(self, item: MenuItem) -> None:
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


class MenuItem:
    """
    A generic menu item
    """

    def __init__(
        self,
        text: str,
        menu: Optional[CursesMenu] = None,
        should_exit: bool = False,
    ):
        """
        :ivar str text: The text shown for this menu item
        :ivar CursesMenu menu: The menu to which this item belongs
        :ivar bool should_exit: Whether the menu should exit once this \
        item's action is done
        """
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self) -> str:
        title = self.menu.title if self.menu else ""
        return f"{title} {self.text}"

    def show(self, index_text: str) -> str:
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
        return f"{index_text} - {self.text}"

    def set_up(self) -> None:
        """
        Override to add any setup actions necessary for the item
        """
        pass

    def action(self) -> None:
        """
        Override to carry out the main action for this item.
        """
        pass

    def clean_up(self) -> None:
        """
        Override to add any cleanup actions necessary for the item
        """
        pass

    def get_return(self) -> Any:
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

    def __init__(self, menu: Optional[CursesMenu] = None):
        super(ExitItem, self).__init__(text="Exit", menu=menu, should_exit=True)

    def show(self, index_text: str) -> str:
        """
        This class overrides this method
        """
        if self.menu and self.menu.parent:
            self.text = "Return to %s menu" % self.menu.parent.title
        else:
            self.text = "Exit"
        return super(ExitItem, self).show(index_text)


class _SelectionItem(MenuItem):
    def __init__(
        self,
        text: str,
        index: int,
        should_exit: bool = False,
        menu: Optional[CursesMenu] = None,
    ):
        super(_SelectionItem, self).__init__(
            text=text,
            should_exit=should_exit,
            menu=menu,
        )
        self.index = index

    def get_return(self) -> int:
        return self.index


def null_input_factory() -> Callable[[int], None]:
    """Create a lambda that takes a single input and does nothing."""
    return lambda input_: None


def clear_terminal() -> None:
    """
    Call the platform specific function to clear the terminal.

    Cls on windows, reset otherwise.
    """
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("reset")
