"""Item that exits a menu or returns to the menu's parent."""

from typing import Optional

from cursesmenu.curses_menu import CursesMenu
from cursesmenu.items.menu_item import MenuItem


class ExitItem(MenuItem):
    """
    The exit item for a menu.

    Changes representation based on whether the menu is a submenu or the root menu.

    :param menu: the menu for this item
    """

    def __init__(
        self,
        menu: Optional[CursesMenu] = None,
        override_index: Optional[str] = None,
    ):
        """Initialize the exit item."""
        super(ExitItem, self).__init__(
            text="Exit",
            menu=menu,
            should_exit=True,
            override_index=override_index,
        )

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
