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

To add other menus as submenus, use a :py:class:`~cursesmenu.items.SubmenuItem`::

    submenu = CursesMenu("This is the submenu")

    submenu_item = SubmenuItem("Show a submenu", submenu, menu=menu)

Add the items to the menu::

    menu.items.append(command_item)

    menu.items.append(function_item)

    menu.items.append(submenu_item)

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

    from cursesmenu CursesMenu

    a_list = ["red", "blue", "green"]

    selection = CursesMenu.get_selection(a_list)

Which is equivalent to::

    from cursesmenu import SelectionMenu

    a_list=["red", "blue", "green"]

    menu = CursesMenu.make_selection_menu(a_list,"Select an option")

    menu.show()

    menu.join()

    selection = menu.selected_option
