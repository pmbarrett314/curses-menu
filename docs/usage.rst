Usage
=====

First things first, import the package::

    import cursesmenu

Or just import what you need::

    from cursesmenu import CursesMenu

    from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem

Then create a menu::

    menu = CursesMenu("This is a menu!", "It has a subtitle too!")

Create menu items for each choice you need::

    command_item = CommandItem("Run a console command", "touch hello.txt")

    function_item = FunctionItem("Call a function", input, ["Enter some input"])

To add other menus as submenus, use a :py:class:`~cursesmenu.items.SubmenuItem`, setting the menu property in the constructor so the submenu's parent is set properly::

    submenu = CursesMenu("This is the submenu")

    submenu_item = SubmenuItem("Show a submenu", submenu, menu=menu)

Add the items to the menu::

    menu.append_item(command_item)

    menu.append_item(function_item)

    menu.append_item(submenu_item)

Then start the menu::

    menu.start()

After that, the menu will spawn its own thread and go about its business. If you want to wait on the user to finish
with the menu before continuing, call::

    menu.join()

To combine these two and simply show a menu and immediately wait for the user to exit the menu, call::

    menu.show()

Getting a selection
-------------------

If you have a list of strings, and you want to allow the user to select one, you can use a
:py:class:`~cursesmenu.SelectionMenu`::

    from cursesmenu import SelectionMenu

    a_list = ["red", "blue", "green"]

    selection = SelectionMenu.get_selection(a_list)

Which is equivalent to::

    from cursesmenu import SelectionMenu

    a_list=["red", "blue", "green"]

    menu = SelectionMenu(a_list,"Select an option")

    menu.show()

    menu.join()

    selection = menu.selected_option

If you want to avoid wasting space, maybe because your screen is really small, you can disable the border
drawn around the menu using the argument `with_border=False`.

    menu = CursesMenu("This is a menu!", "It has a subtitle too!", with_border=False)

Furthermore some spacings, like between title and subtitle and in front of menu items, will not appear
when the `tight=True` is passed to the menu constructors.

    menu = CursesMenu("This is a menu!", "It has a subtitle too!", tight=True)

These two options are also available for :py:class:`~cursesmenu.SelectionMenu`.
