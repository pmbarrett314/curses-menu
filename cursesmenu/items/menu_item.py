"""Base class for menu items."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from cursesmenu.curses_menu import CursesMenu


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
        menu: CursesMenu | None = None,
        *,
        should_exit: bool = False,
        override_index: str | None = None,
    ) -> None:
        """Initialize the menu item."""
        self.text = text
        self.menu = menu
        self.should_exit = should_exit
        self.override_index = override_index

    def show(self, index_text: str) -> str:
        """
        Provide the representation that should be used for this item in a menu.

        The base class is simply "[index] - [text]"

        :param index_text: The string used for the index, provided by the menu.
        :return: The text representing the item.
        """
        if self.override_index is not None:
            index_text = self.override_index
        return f"{index_text} - {self.text}"

    def set_up(self) -> None:
        """Perform setup for the item."""

    def action(self) -> None:
        """
        Do the main action for the item.

        If you're just writing a simple subclass, you shouldn't need set_up or clean_up.
        The menu just calls them in order. They are provided so you can make subclass
        hierarchies where the superclass handles some setup and cleanup for its
        subclasses.
        """

    def clean_up(self) -> None:
        """Perform cleanup for the item."""

    def get_return(self) -> Any:  # noqa: ANN401
        """
        Get the return value for this item.

        For a basic MenuItem, just forwards the return value from the menu.

        :return: The return value for the item.
        """
        if self.menu:
            return self.menu.returned_value
        return None

    def __str__(self) -> str:
        """Get a basic string representation of the item."""
        title = self.menu.title if self.menu else ""
        return f"{title} {self.text}"
