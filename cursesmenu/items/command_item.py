"""A  menu item that runs a shell command."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from cursesmenu.items.external_item import ExternalItem

if TYPE_CHECKING:
    import os
    from typing import Any

    from cursesmenu.curses_menu import CursesMenu

    PathType = os.PathLike[Any]


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
        arguments: list[str] | None = None,
        menu: CursesMenu | None = None,
        *,
        should_exit: bool = False,
        override_index: str | None = None,
        stdout_filepath: PathType | None = None,
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
        self.arguments: list[str]
        if arguments:
            self.arguments = arguments
        else:
            self.arguments = []
        self.kwargs = kwargs

        if stdout_filepath:
            self.stdout_filepath: Path | None = Path(stdout_filepath)
        else:
            self.stdout_filepath = None

        self.exit_status: int | None = None

    def _get_args_list(self) -> list[str]:
        args = [self.command, *self.arguments]
        if not sys.platform.startswith("win"):  # pragma: no-cover-windows
            return [" ".join(args)]
        else:  # pragma: no-cover-nonwindows
            return args

    def action(self) -> None:
        """Run the command using subprocess.run."""
        args = self._get_args_list()

        if self.stdout_filepath:
            with self.stdout_filepath.open("w") as stdout:
                completed_process = subprocess.run(
                    args,
                    shell=True,
                    stdout=stdout,
                    check=False,
                    **self.kwargs,
                )
        else:
            completed_process = subprocess.run(
                args,
                shell=True,
                check=False,
                **self.kwargs,
            )
        self.exit_status = completed_process.returncode

    def get_return(self) -> int | None:
        """Get the exit status of the command or None if it hasn't been run."""
        return self.exit_status
