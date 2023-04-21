"""A menu item that executes a Python function with arguments."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cursesmenu.items.external_item import ExternalItem

if TYPE_CHECKING:
    from typing import Any, Callable

    from cursesmenu.curses_menu import CursesMenu


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
        args: list[Any] | None = None,
        kwargs: dict[Any, Any] | None = None,
        menu: CursesMenu | None = None,
        *,
        should_exit: bool = False,
        override_index: str | None = None,
    ) -> None:
        """Initialize the item."""
        super().__init__(
            text=text,
            menu=menu,
            should_exit=should_exit,
            override_index=override_index,
        )
        self.function = function
        if args is None:
            args = []
        self.args: list[Any] = args
        if kwargs is None:
            kwargs = {}
        self.kwargs: dict[Any, Any] = kwargs

        self.return_value: Any = None

    def action(self) -> None:
        """Call the function with the provided arguments."""
        self.return_value = self.function(*self.args, **self.kwargs)

    def get_return(self) -> Any:  # noqa: ANN401
        """
        Get the returned value from the function.

        :return: The value returned from the function, or None if it hasn't been called.
        """
        return self.return_value
