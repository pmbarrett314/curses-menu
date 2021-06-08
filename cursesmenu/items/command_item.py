import os
import subprocess
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
    A menu item to execute a console command
    """

    def __init__(
        self,
        text: str,
        command: str,
        arguments: Optional[List[str]] = None,
        menu: Optional[CursesMenu] = None,
        should_exit: bool = False,
        stdout_filepath: Optional[PathType] = None,
        **kwargs: Any,
    ):
        """
        :ivar str command: The console command to be executed
        :ivar list[str] arguments: An optional list of string arguments to be passed \
        to the command
        :ivar int exit_status: the exit status of the command, None if it hasn't \
        been run yet
        """
        super(CommandItem, self).__init__(text=text, menu=menu, should_exit=should_exit)
        self.command = command
        self.arguments: List[str]
        if arguments:
            self.arguments = arguments
        else:
            self.arguments = []
        self.kwargs = kwargs
        self.stdout_filepath = stdout_filepath
        self.exit_status: Optional[int] = None

    def action(self) -> None:
        """
        This class overrides this method
        """
        args = [self.command] + self.arguments
        if self.stdout_filepath:
            with open(self.stdout_filepath, "w") as stdout:
                completed_process = subprocess.run(
                    args, shell=True, stdout=stdout, **self.kwargs
                )
        else:
            completed_process = subprocess.run(args, shell=True, **self.kwargs)
        self.exit_status = completed_process.returncode

    def get_return(self) -> Optional[int]:
        """
        :return: the exit status of the command
        :rtype: int
        """
        return self.exit_status
