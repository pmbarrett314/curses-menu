"""A class for a menu item with an integer return value."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cursesmenu.items import MenuItem

if TYPE_CHECKING:
    from cursesmenu import CursesMenu
else:
    CursesMenu = Any


class SelectionItem(MenuItem):
    """A class for a menu item with an integer return value."""

    def __init__(
        self,
        text: str,
        index: int,
        menu: CursesMenu | None = None,
        *,
        should_exit: bool = False,
        override_index: str | None = None,
    ) -> None:
        """Initialize the item."""
        super().__init__(
            text=text,
            should_exit=should_exit,
            menu=menu,
            override_index=override_index,
        )
        self.index = index

    def get_return(self) -> int:
        """Get the return value."""
        return self.index
