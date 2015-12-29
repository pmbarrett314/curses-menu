Usage
=====

First things first, import the package::

    import cursesmenu

Or just import what you need::

    from cursesmenu import CursesMenu

    from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem

Then create a menu::

    menu = CursesMenu(title="This is a menu!", subtitle="It has a subtitle too!")

Create some items::

    command_item = CommandItem("command", menu, "touch hello.txt")

    function_item = FunctionItem("function", menu, input,["Enter some input"])

Maybe even a submenu::

    submenu = CursesMenu(title="This is the submenu")

    submenu_item = SubmenuItem("submenu", menu, submenu)

Add the items to the menu::

    menu.append_item(command_item)

    menu.append_item(function_item)

    menu.append_item(submenu_item)

Then show the menu::

    menu.show()

And let the user take over from there.

Getting a selection
-------------------

If you'd like to get a selection from a list, that's even easier::

    from cursesmenu import SelectionMenu

    a_list=["red", "blue", "green"]

    selection=SelectionMenu.get_selection(a_list)

