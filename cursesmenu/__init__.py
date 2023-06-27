import sys
from importlib import metadata

from . import items
from .curses_menu import CursesMenu
from .item_group import ItemGroup

__all__ = ["CursesMenu", "ItemGroup", "items"]

__version__ = metadata.version("curses-menu")

del metadata, sys
