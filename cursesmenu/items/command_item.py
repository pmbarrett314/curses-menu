"""A  menu item that runs a shell command."""

import os
import subprocess
import sys
from typing import TYPE_CHECKING, Any, List, Optional

from cursesmenu.items.external_item import ExternalItem

if TYPE_CHECKING:
    from cursesmenu.curses_menu import CursesMenu

    PathType = os.PathLike[Any]
else:
    CursesMenu = Any
    PathType = Any


class CommandItem(ExternalItem):
    """
    A  menu item that runs a shell command using subprocess.run.

    :param text: The text for the menu item.
    :param command: The shell command to run when the item is selected.
    :param arguments: Additional arguments passed to the command.
    :param menu: The menu that this item belongs to
    :param should_exit: Whether the menu will exit when this item is selected
    :param stdout_filepath: A filepath that the stdout for the command will be written \
    to
    :param kwargs: A list of kwargs to be passed to subprocess.run
    """

    def __init__(
        self,
        text: str,
        command: str,
        arguments: Optional[List[str]] = None,
        menu: Optional[CursesMenu] = None,
        *,
        should_exit: bool = False,
        override_index: Optional[str] = None,
        stdout_filepath: Optional[PathType] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Initialize the menu."""
        super().__init__(
            text=text,
            menu=menu,
            should_exit=should_exit,
            override_index=override_index,
        )
        self.command = command
        self.arguments: List[str]
        if arguments:
            self.arguments = arguments
        else:
            self.arguments = []
        self.kwargs = kwargs
        self.stdout_filepath = stdout_filepath
        self.exit_status: Optional[int] = None

    def _get_args_list(self) -> List[str]:
        args = [self.command] + self.arguments
        if not sys.platform.startswith("win"):  # pragma: no-cover-windows
            return [" ".join(args)]
        else:  # pragma: no-cover-nonwindows
            return args

    def action(self) -> None:
        """Run the command using subprocess.run."""
        args = self._get_args_list()

        if self.stdout_filepath:
            with open(self.stdout_filepath, "w") as stdout:
                completed_process = subprocess.run(
                    args, shell=True, stdout=stdout, **self.kwargs
                )
        else:
            completed_process = subprocess.run(args, shell=True, **self.kwargs)
        self.exit_status = completed_process.returncode

    def get_return(self) -> Optional[int]:
        """Get the exit status of the command or None if it hasn't been run."""
        return self.exit_status
