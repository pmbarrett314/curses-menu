"""Utility functions for curses-menu."""

import os
import sys
from typing import Callable


def null_input_factory() -> Callable[[int], None]:
    """Create a lambda that takes a single input and does nothing."""
    return lambda input_: None


def clear_terminal() -> None:
    """
    Call the platform specific function to clear the terminal.

    Cls on windows, reset otherwise.
    """
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("reset")


def soft_clear_terminal() -> None:
    """Use ANSI control sequences to clear the terminal."""
    if sys.platform.startswith("win"):  # pragma: no cover all
        # enables ANSI escape codes to work properly in bare cmd.exe
        os.system("")
    print(chr(27) + "[2J", end="")
    print(chr(27) + "[1;1H", end="")
