import curses
from typing import TYPE_CHECKING, Any, Optional

from cursesmenu.curses_menu import MenuItem

if TYPE_CHECKING:
    from cursesmenu.curses_menu import CursesMenu
else:
    CursesMenu = Any


class SubmenuItem(MenuItem):
    """
    A menu item to open a submenu
    """

    def __init__(
        self,
        text: str,
        submenu: Optional[CursesMenu] = None,
        menu: Optional[CursesMenu] = None,
        should_exit: bool = False,
    ):
        """
        :ivar CursesMenu self.submenu: The submenu to be opened when \
        this item is selected
        """
        self._submenu: Optional[CursesMenu] = submenu
        self._menu: Optional[CursesMenu] = menu
        if self._submenu:
            self._submenu.parent = menu
        super(SubmenuItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

    @property
    def submenu(self) -> Optional[CursesMenu]:
        return self._submenu

    @submenu.setter
    def submenu(self, submenu: Optional[CursesMenu]) -> None:
        self._submenu = submenu
        if self._submenu is not None:
            self._submenu.parent = self._menu

    @property  # type: ignore[override]
    def menu(self) -> Optional[CursesMenu]:  # type: ignore[override]
        return self._menu

    @menu.setter
    def menu(self, menu: Optional[CursesMenu]) -> None:
        self._menu = menu
        if self._submenu is not None:
            self._submenu.parent = menu

    def set_up(self) -> None:
        """
        This class overrides this method
        """
        assert self.menu is not None
        self.menu.pause()
        curses.def_prog_mode()
        self.menu.clear_screen()

    def action(self) -> None:
        """
        This class overrides this method
        """
        assert self.submenu is not None
        self.submenu.start()

    def clean_up(self) -> None:
        """
        This class overrides this method
        """
        assert self.menu is not None
        assert self.submenu is not None
        self.submenu.join()
        self.menu.clear_screen()
        curses.reset_prog_mode()
        curses.curs_set(1)  # reset doesn't do this right
        curses.curs_set(0)
        self.menu.resume()

    def get_return(self) -> Any:
        """
        :return: The returned value in the submenu
        """
        if self.submenu is not None:
            return self.submenu.returned_value
        return None
