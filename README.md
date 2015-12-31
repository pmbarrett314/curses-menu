[![Build Status](https://travis-ci.com/pmbarrett314/curses-menu.svg?token=eWX7zFvhdYRJVxPoXia3&branch=master)](https://travis-ci.com/pmbarrett314/curses-menu)[![Documentation Status](https://readthedocs.org/projects/curses-menu/badge/?version=latest)](http://curses-menu.readthedocs.org/en/latest/?badge=latest)

# curses-menu
A simple Python menu-based GUI system on the terminal using curses. Perfect for those times when you need a GUI, but don't want the overhead or learning curve of a full-fledged GUI framework.

http://curses-menu.readthedocs.org/en/latest/

### Installation
Currently only supports Python 3.5.

The curses library comes bundled with python on Linux and MacOS. Windows users can visit http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses and get a third-party build for your platform and Python version.

Then just run python setup.py install from the project directory. PyPi coming soon.

## Usage
It's designed to be pretty simple to use. Here's an example

```Python
# import the necessary packages
from cursesmenu import *
from cursesmenu.items import *

# create the menu
menu = CursesMenu("Title", "Subtitle")
# create various items, MenuItem is the base class for all items, it doesn't do anything when selected
item1 = MenuItem("Item", menu)
# a FunctionItem runs a Python function when selected, a CommandItem runs a console command
function_item = FunctionItem("Fun item", menu, input, ["Enter an input"])
command_item = CommandItem("Command", menu, "echo hello")
# a SelectionMenu constructs a menu from a list of strings
submenu = SelectionMenu(["item1", "item2", "item3"])
# a SubmenuItem lets you add a menu as a submenu of another menu
submenu_item = SubmenuItem("Submenu item", menu, submenu)
# once we're done creating them, we just add the items to the menu
menu.append_item(item1)
menu.append_item(function_item)
menu.append_item(command_item)
menu.append_item(submenu_item)
# finally, we call show to show the menu and allow the user to interact
menu.show()
```
