"""Top level class and functions for a curses-based menu."""

import atexit
import curses
import os
import pathlib
import threading
import time
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, DefaultDict, List, Optional, cast

from deprecated import deprecated

import cursesmenu.utils
from cursesmenu.item_group import ItemGroup

if TYPE_CHECKING:
    # noinspection PyCompatibility,PyProtectedMember
    from _curses import window

    Window = window
    from cursesmenu.items.menu_item import MenuItem
else:
    Window = Any
    MenuItem = Any

MIN_SIZE = 6  # Top bar, space, title, space, subtitle, space, bottom bar

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()


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
    :param show_exit_item: Whether the exit item is shown
    :param zero_pad: Zero pad the item indices to match the width of the biggest one
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
        *,
        show_exit_item: bool = True,
        zero_pad: bool = False,
        _debug_screens: bool = False,
    ):
        """Initialize the menu."""
        self.title = title
        self.subtitle = subtitle
        self.zero_pad = zero_pad

        self.screen: Optional[Window] = None

        # highlight should be initialized to black-on-white, but bold is a fine
        # fallback that doesn't need the screen initialized first
        self.highlight: int = curses.A_BOLD
        self.normal: int = curses.A_NORMAL

        # TODO: add a way to replace item indices with letters
        self.items: ItemGroup = ItemGroup(self)
        self.end_items: ItemGroup = ItemGroup(self)
        if show_exit_item:
            from cursesmenu.items.exit_item import ExitItem

            self.end_items.append(ExitItem(menu=self, override_index="q"))

        self.current_option = 0
        self.selected_option = -1

        self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)

        self._running = threading.Event()
        self.should_exit = False

        # TODO: Should this be a property
        self.returned_value = None

        self.parent: Optional[CursesMenu] = None

        self.user_input_handlers: DefaultDict[int, Callable[[int], None]] = defaultdict(
            cursesmenu.utils.null_input_factory,
        )
        self.user_input_handlers.update(
            {
                ord("\n"): self.select,
                curses.KEY_UP: self.go_up,
                curses.KEY_DOWN: self.go_down,
                ord("q"): self.go_to_exit,
                curses.KEY_RESIZE: self.on_resize,
            },
        )
        # workaround for issue with windows-curses in vscode terminal
        if (
            os.environ.get("TERM_PROGRAM", default="") == "vscode"
        ):  # pragma: no cover all
            self.user_input_handlers.update(
                {
                    450: self.go_up,
                    456: self.go_down,
                },
            )
        self.user_input_handlers.update(
            {k: self.go_to for k in map(ord, map(str, range(1, 10)))},
        )

        self._debug_screens = _debug_screens

    def __repr__(self) -> str:
        """Get a string representation of the menu."""
        return f"<{self.title}: {self.subtitle}. {len(self.items)} items>"

    @classmethod
    def make_selection_menu(
        cls,
        selections: List[str],
        title: str = "",
        subtitle: str = "",
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
        from cursesmenu.items.selection_item import SelectionItem

        for index, selection in enumerate(selections):
            menu.items.append(
                SelectionItem(text=selection, index=index, should_exit=True),
            )
        return menu

    @classmethod
    def get_selection(
        cls,
        selections: List[str],
        title: str = "",
        subtitle: str = "",
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
    def all_items(self) -> ItemGroup:
        """Get the combined list of items."""
        return self.items + self.end_items

    @property
    def current_item(self) -> Optional[MenuItem]:
        """Get the currently selected MenuItem."""
        if not self.all_items:
            return None
        else:
            return self.all_items[self.current_option]

    @property
    def selected_item(self) -> Optional[MenuItem]:
        """Get the most recently selected MenuItem."""
        if self.selected_option == -1:
            return None
        else:
            return self.all_items[self.selected_option]

    @property
    def menu_height(self) -> int:
        """Get the number of items to be shown."""
        return len(self.all_items) + MIN_SIZE

    @property
    def last_item_index(self) -> int:
        """Get the index of the last item in a list of items including the exit item \
        if it's shown."""
        return len(self.all_items) - 1

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
        self.should_exit = False
        self._main_thread = threading.Thread(target=self._wrap_start, daemon=True)
        self._main_thread.start()

    def _wrap_start(self) -> None:
        if self.parent is None:
            cursesmenu.utils.soft_clear_terminal()

            # We only want to fully clear the screen at the exit of the outermost\
            # Script that uses curses to prevent character handling from messing up
            if os.getenv("CURSES_MENU_PID") is None:
                pid = os.getpid()
                os.environ["CURSES_MENU_PID"] = str(pid)
                atexit.register(cursesmenu.utils.clear_terminal)

            try:
                CursesMenu.stdscr = curses.initscr()
                curses.noecho()
                curses.cbreak()
                CursesMenu.stdscr.keypad(True)
                # noinspection PyBroadException
                try:
                    curses.start_color()
                except:  # noqa: E722 # pragma: no cover all
                    pass
                self._main_loop()
            finally:
                # I currently don't remember whether there's a situation where stdscr
                # should be None at runtime, so I'm leaving this as an if
                # as opposed to an assert, but using a pragma for coverage
                if CursesMenu.stdscr is not None:  # pragma: no branch
                    CursesMenu.stdscr.keypad(False)
                curses.endwin()
                curses.echo()
                curses.nocbreak()
                os.system("stty echo")
        else:
            self._main_loop()

    def _main_loop(self) -> None:
        assert CursesMenu.stdscr is not None
        self.screen = curses.newpad(self.menu_height, CursesMenu.stdscr.getmaxyx()[1])
        self._set_up_colors()
        curses.curs_set(0)
        CursesMenu.stdscr.refresh()
        self.draw()

        self._running.set()
        while self._running.wait() is not False and not self.should_exit:
            CursesMenu.currently_active_menu = self
            self.process_user_input()
        self.clear_screen()
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
        self.screen.border()
        self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        for index, item in enumerate(self.all_items):
            self.draw_item(index, item)

        self.refresh_screen()
        if self._debug_screens:  # pragma: no cover all
            with open(
                PROJECT_ROOT.joinpath("screendumps", f"{self.title}-{time.time()}"),
                "wb",
            ) as f:
                self.screen.putwin(f)
            with open(
                PROJECT_ROOT.joinpath(
                    "screendumps",
                    f"stdscr-{self.title}-{time.time()}",
                ),
                "wb",
            ) as f:
                self.screen.putwin(f)

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
            if self.zero_pad:
                pad_width = len(str(len(self.items)))
                index_text = index_text.zfill(pad_width)

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
        if not self.all_items:
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

        Called on numerical input. Currently implementation only works on single digits.
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
        self.current_option = self.last_item_index
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

    def on_resize(self, _: int = 0) -> None:
        """Handle a terminal resize event."""
        assert CursesMenu.stdscr is not None
        screen_rows, screen_cols = CursesMenu.stdscr.getmaxyx()
        curses.resizeterm(screen_rows, screen_cols)
        self.draw()

    def clear_screen(self) -> None:
        """Clear the screen for this menu."""
        assert self.screen is not None
        self.screen.clear()
        self.refresh_screen()

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

    def adjust_screen_size(self) -> None:
        """Adjust the screen size to match the length of the item list and redraw."""
        if self.screen:
            max_row, max_cols = self.screen.getmaxyx()
            if max_row < MIN_SIZE + len(self.all_items):
                self.screen.resize(self.menu_height, max_cols)
            self.draw()

    @deprecated(reason="Use self.items.append.", version="0.6.0")
    def append_item(self, item: MenuItem) -> None:
        """Append an item to the list of items."""
        self.items.append(item)
