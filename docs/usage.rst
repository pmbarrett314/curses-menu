Usage
=====

First things first, import the package::

    import cursesmenu

Or just import what you need::

    from cursesmenu import CursesMenu

    from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem

Then create a menu::

    menu = CursesMenu(title="This is a menu!", subtitle="It has a subtitle too!")

Create menu items for each choice you need::

    command_item = CommandItem("command", menu, "touch hello.txt")

    function_item = FunctionItem("function", menu, input,["Enter some input"])

If you'd like to add submenus, just create a :py:class:`~cursesmenu.items.SubmenuItem`::

    submenu = CursesMenu(title="This is the submenu")

    submenu_item = SubmenuItem("submenu", menu, submenu)

Add the items to the menu::

    menu.append_item(command_item)

    menu.append_item(function_item)

    menu.append_item(submenu_item)

Then call show to start the menu::

    menu.show()

After that, the menu will spawn its own thread and go about its business. If you want to wait on the user to finish
with the menu before continuing, call::

    menu.join()

Getting a selection
-------------------

If you have a list of things (strings for example), and you want to allow the user to select one, you can use a
:py:class:`~cursesmenu.SelectionMenu`::

    from cursesmenu import SelectionMenu

    a_list=["red", "blue", "green"]

    selection=SelectionMenu.get_selection(a_list)

