from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from cursesmenu.items.external_item import ExternalItem

if TYPE_CHECKING:
    from cursesmenu.curses_menu import CursesMenu
else:
    CursesMenu = Any


class FunctionItem(ExternalItem):
    """
    A menu item to call a Python function
    """

    def __init__(
        self,
        text: str,
        function: Callable[..., Any],
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[Any, Any]] = None,
        menu: Optional[CursesMenu] = None,
        should_exit: bool = False,
    ):
        """
        :ivar function: The function to be called
        :ivar list args: An optional list of arguments to be passed to the function
        :ivar dict kwargs: An optional dictionary of keyword arguments to be passed \
        to the function
        :ivar return_value: the value returned by the function, \
        None if it hasn't been called yet.
        """
        super(FunctionItem, self).__init__(
            text=text,
            menu=menu,
            should_exit=should_exit,
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
        """
        This class overrides this method
        """
        self.return_value = self.function(*self.args, **self.kwargs)

    def get_return(self) -> Any:
        """
        :return: The return value from the function call
        """
        return self.return_value
