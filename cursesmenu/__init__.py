import sys

if sys.version_info[:2] >= (3, 8):  # pragma: py-lt-38
    from importlib import metadata
else:  # pragma: py-gte-38
    import importlib_metadata as metadata

from . import items
from .curses_menu import CursesMenu
from .item_group import ItemGroup

__all__ = ["CursesMenu", "ItemGroup", "items"]

__version__ = metadata.version("curses-menu")

del metadata, sys
