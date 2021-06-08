"""Top level class and functions for a curses-based menu."""

import curses
import threading
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, DefaultDict, List, Optional, cast

from cursesmenu.utils import clear_terminal, null_input_factory

if TYPE_CHECKING:
    # noinspection PyCompatibility,PyProtectedMember
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    Window = Any
    MenuItem = Any

MIN_SIZE = 6  # Top bar, space, title, space, subtitle, space, bottom bar


class CursesMenu:
    """
    A menu created with the curses library.

    :param title: The title of the menu
    :param subtitle: The menu subtitle
    :ivar screen: The curses window associated with the menu. \
    Created using curses.newpad when the menu is started
    :ivar highlight: Index of the curses color pair\
    used to represent the highlighted item
    :ivar normal: Index of the curses color pair used to represent other text
    :ivar items: The list of items for the menu
    :ivar exit_item: The ExitItem for this menu, will be displayed last.
    :param show_exit_item: Whether the exit item is shown
    :ivar current_option: The index of the currently highlighted menu item
    :ivar selected_option: The index of the last item the user selected, initially -1
    :ivar should_exit: Flag to signal that the menu should exit on \
    its next pass through its main loop
    :ivar returned_value: The value returned by the last selected item
    :ivar parent: The parent menu of this one, or None if this menu is the root menu
    :ivar user_input_handlers: A dictionary mapping character values to functions \
    that handle those characters
    :ivar current_item: The MenuItem that's currently highlighted
    :ivar selected_item: The Menu item that's currently selected
    :cvar stdscr: The root curses window
    :ivar menu_height: The total height of the menu including the exit item
    :ivar last_item_index: The index of the max item in the menu, \
    including the exit item
    :cvar currently_active_menu: Class variable that holds the \
    currently active menu or None if no menu\
    is currently active (E.G. when switching between menus)
    """

    currently_active_menu: Optional["CursesMenu"] = None
    stdscr: Optional[Window] = None

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        show_exit_item: bool = True,
    ):
        """Initialize the menu."""
        self.title = title
        self.subtitle = subtitle

        self.screen: Optional[Window] = None

        # highlight should be initialized to black-on-white, but bold is a fine
        # fallback that doesn't need the screen initialized first
        self.highlight: int = curses.A_BOLD
        self.normal: int = curses.A_NORMAL

        # TODO: add a list of items that floats at the end
        # TODO: add a way to replace item indices with letters
        # TODO: instead of  conditionally adding 1 for exit item, just combine
        #  the regular list and the floating one
        #  this way the consumer can add their own floating exit item
        self.items: List[MenuItem] = []

        self.exit_item = ExitItem(menu=self)
        self.show_exit_item = show_exit_item

        self.current_option = 0
        self.selected_option = -1

        self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)

        self._running = threading.Event()
        # TODO:should this just depend on the thread?
        self.should_exit = False

        # TODO: Should this be a property
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

    def __repr__(self) -> str:
        """Get a string representation of the menu."""
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
        """Get the currently selected MenuItem."""
        if self.current_option == len(self.items) and self.show_exit_item:
            return self.exit_item
        elif self.items:
            return self.items[self.current_option]
        else:
            return None

    @property
    def selected_item(self) -> Optional[MenuItem]:
        """Get the most recently selected MenuItem."""
        if self.selected_option == -1:
            return None
        elif self.selected_option == len(self.items) and self.show_exit_item:
            return self.exit_item
        else:
            return self.items[self.selected_option]

    @property
    def menu_height(self) -> int:
        """Get the number of items to be shown."""
        return len(self.items) + MIN_SIZE + (1 if self.show_exit_item else 0)

    @property
    def last_item_index(self) -> int:
        """Get the index of the last item in a list of items including the exit item \
        if it's shown."""
        return len(self.items) if self.show_exit_item else len(self.items) - 1

    def show(self) -> Any:
        """
        Start the menu and blocks until it finishes.

        :return: The return value from the last selected item
        """
        self.start()
        return self.join()

    def start(self) -> None:
        """
        Start the menu's thread and return without blocking.

        The menu's thread is a daemon, so if the calling script \
        may exit before the user is finished interacting, use \
        :meth:`join()<cursesmenu.CursesMenu.join>` to block until the menu exits.
        """
        self._main_thread.start()

    def _wrap_start(self) -> None:
        try:
            if self.parent is None:
                curses.wrapper(self._main_loop)
            else:
                self._main_loop(None)
        finally:
            self.clear_screen()
            clear_terminal()

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

        self._running.set()
        while self._running.wait() is not False and not self.should_exit:
            CursesMenu.currently_active_menu = self
            self.process_user_input()
        self._running.clear()

    def _set_up_colors(self) -> None:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)

    def draw(self) -> None:
        """
        Draw the menu.

        Adds border, title and subtitle, and items, then refreshes the screen.
        """
        assert self.screen is not None
        self.screen.border(0)
        self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.items):
            self.draw_item(index, item)

        if self.show_exit_item:
            # TODO: Replace this logic with like a dictionary of replacements
            self.draw_item(len(self.items), self.exit_item, "q")

        self.refresh_screen()

    def draw_item(
        self,
        index: int,
        item: MenuItem,
        index_text: Optional[str] = None,
    ) -> None:
        """
        Draw an individual item.

        :param index: The numerical index of the item in the list
        :param item: The item to be drawn
        :param index_text: Text to override the index portion of the item
        """
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
        """Refresh what's onscreen to match the cursor's position."""
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
        Get and then handle the user's input.

        :return: The character the user input.
        """
        user_input = self.get_input()
        self.user_input_handlers[user_input](user_input)
        return user_input

    # noinspection PyMethodMayBeStatic
    def get_input(self) -> int:
        """
        Get the user's input.

        :return: The character input by the user.
        """
        assert CursesMenu.stdscr is not None
        return CursesMenu.stdscr.getch()

    def select(self, _: int = 0) -> None:
        """
        Select the current item.

        Called for the enter/return key.
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
        Go to a given numbered item.

        Called on numerical input. Currently implentation only works on single digits.
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
        """
        Go to the exit item.

        Called for Q.
        """
        if self.show_exit_item:
            self.current_option = len(self.items)
            self.draw()

    def go_down(self, _: int = 0) -> None:
        """
        Go down one item, wrap if necessary.

        Called when the user presses the down arrow.
        """
        if self.current_option < self.last_item_index:
            self.current_option += 1
        else:
            self.current_option = 0
        self.draw()

    def go_up(self, _: int = 0) -> None:
        """
        Go up one item, wrap if necessary.

        Called when the user presses the up arrow.
        """
        if self.current_option > 0:
            self.current_option += -1
        else:
            self.current_option = self.last_item_index
        self.draw()

    def clear_screen(self) -> None:
        """Clear the screen for this menu."""
        assert self.screen is not None
        self.screen.clear()

    def join(self, timeout: Optional[int] = None) -> Any:
        """
        Block until the menu exits.

        :param timeout: time in seconds until the menu is forced to close
        :return: The value returned from the last selected item
        """
        self._main_thread.join(timeout=timeout)
        return self.returned_value

    def is_running(self) -> bool:
        """
        Check if the menu has is running (has not been paused).

        :return: True if the menu has not been paused false otherwise.
        """
        return self._running.is_set()

    def wait_for_start(self, timeout: Optional[int] = None) -> bool:
        """
        Block until the menu starts.

        :param timeout: Timeout in seconds
        :return: True unless the operation times out
        """
        return self._running.wait(timeout)

    def pause(self) -> None:
        """Pause this menu's thread."""
        self._running.clear()

    def resume(self) -> None:
        """Resume this menu's thread."""
        self._running.set()

    def is_alive(self) -> bool:
        """
        Check if the menu's thread is running.

        :return: True if the menu's thread is alive, false if not.
        """
        return self._main_thread.is_alive()

    def exit(self, timeout: Optional[int] = None) -> Any:
        """
        Signal the menu to exit and block until it does.

        :param timeout: timeout before the menu is forced to close
        :return: the value of the last selected item
        """
        self._exit()
        return self.join(timeout)

    def append_item(self, item: MenuItem) -> None:
        """
        Append an item to the menu and redraw.

        :param item: A MenuItem to append to the list
        """
        item.menu = self
        self.items.append(item)
        # TODO: Define subclass of ABC.orderedcollection to hold items
        if self.screen:
            max_row, max_cols = self.screen.getmaxyx()
            if max_row < MIN_SIZE + len(self.items):
                self.screen.resize(self.menu_height, max_cols)
            self.draw()


class MenuItem:
    """
    The base class for menu items.

    Is displayed in a basic manner and does nothing when selected.

    :param text: The text representing this menu item
    :param should_exit: Whether the menu should exit when this item is selected
    :param menu: The menu that owns this item
    """

    def __init__(
        self,
        text: str,
        menu: Optional[CursesMenu] = None,
        should_exit: bool = False,
    ):
        """Initialize the menu item."""
        self.text = text
        self.menu = menu
        self.should_exit = should_exit

    def __str__(self) -> str:
        """Get a basic string representation of the item."""
        title = self.menu.title if self.menu else ""
        return f"{title} {self.text}"

    def show(self, index_text: str) -> str:
        """
        Provide the representation that should be used for this item in a menu.

        The base class is simply "[index] - [text]"

        :param index_text: The string used for the index, provided by the menu.
        :return: The text representing the item.
        """
        return f"{index_text} - {self.text}"

    def set_up(self) -> None:
        """Perform setup for the item."""
        pass

    def action(self) -> None:
        """
        Do the main action for the item.

        If you're just writing a simple subclass, you shouldn't need set_up or clean_up.
        The menu just calls them in order. They are provided so you can make subclass
        hierarchies where the superclass handles some setup and cleanup for its
        subclasses.
        """
        pass

    def clean_up(self) -> None:
        """Perform cleanup for the item."""
        pass

    def get_return(self) -> Any:
        """
        Get the return value for this item.

        For a basic MenuItem, just forwards the return value from the menu.

        :return: The return value for the item.
        """
        if self.menu:
            return self.menu.returned_value
        return None


class ExitItem(MenuItem):
    """
    The exit item for a menu.

    Changes representation based on whether the menu is a submenu or the root menu.

    :param menu: the menu for this item
    """

    def __init__(self, menu: Optional[CursesMenu] = None):
        """Initialize the exit item."""
        super(ExitItem, self).__init__(text="Exit", menu=menu, should_exit=True)

    def show(self, index_text: str) -> str:
        """
        Get the representation of this item \
        dependent on whether it's in a submenu or the root menu.

        :param index_text:
        :return: The representation of this item
        """
        if self.menu and self.menu.parent:
            # TODO: implement an item that exits the whole menu
            #  hierarchy from a submenu.
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
