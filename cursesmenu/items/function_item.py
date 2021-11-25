"""A menu item that executes a Python function with arguments."""

from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from cursesmenu.items.external_item import ExternalItem

if TYPE_CHECKING:
    from cursesmenu.curses_menu import CursesMenu
else:
    CursesMenu = Any


class FunctionItem(ExternalItem):
    """
    A menu item that executes a Python function with arguments.

    :param text: The text of the item
    :param function: A function or lambda to be executed when the item is selected
    :param args: A list of poitional arguments to be passed to the function
    :param kwargs: A dict of kwargs to be passed to the function
    :param menu: The menu that this item belongs to
    :param should_exit: Whether the menu will exit when this item is selected
    """

    def __init__(
        self,
        text: str,
        function: Callable[..., Any],
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[Any, Any]] = None,
        menu: Optional[CursesMenu] = None,
        should_exit: bool = False,
        override_index: Optional[str] = None,
    ):
        """Initialize the item."""
        super(FunctionItem, self).__init__(
            text=text,
            menu=menu,
            should_exit=should_exit,
            override_index=override_index,
        )
        self.function = function
        if args is None:
            args = []
        self.args: List[Any] = args
        if kwargs is None:
            kwargs = {}
        self.kwargs: Dict[Any, Any] = kwargs

        self.return_value: Any = None

    def action(self) -> None:
        """Call the function with the provided arguments."""
        self.return_value = self.function(*self.args, **self.kwargs)

    def get_return(self) -> Any:
        """
        Get the returned value from the function.

        :return: The value returned from the function, or None if it hasn't been called.
        """
        return self.return_value
