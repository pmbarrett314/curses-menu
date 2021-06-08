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
