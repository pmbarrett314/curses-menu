CursesMenu --- Standard menu class
==================================

.. autoclass:: cursesmenu.CursesMenu

    .. automethod:: cursesmenu.CursesMenu.start
    .. automethod:: cursesmenu.CursesMenu.join
    .. automethod:: cursesmenu.CursesMenu.show

    .. raw:: html

        <h2>Item Management</h2>

    .. automethod:: cursesmenu.CursesMenu.append_item

    .. raw:: html

        <h2>User interaction</h2>

    .. automethod:: cursesmenu.CursesMenu.get_input
    .. automethod:: cursesmenu.CursesMenu.process_user_input
    .. automethod:: cursesmenu.CursesMenu.draw
    .. automethod:: cursesmenu.CursesMenu.go_to
    .. automethod:: cursesmenu.CursesMenu.go_up
    .. automethod:: cursesmenu.CursesMenu.go_down
    .. automethod:: cursesmenu.CursesMenu.select
    .. automethod:: cursesmenu.CursesMenu.exit

    .. raw:: html

        <h2>State management</h2>

    .. automethod:: cursesmenu.CursesMenu.is_alive
    .. automethod:: cursesmenu.CursesMenu.wait_for_start
    .. automethod:: cursesmenu.CursesMenu.pause
    .. automethod:: cursesmenu.CursesMenu.resume
    .. automethod:: cursesmenu.CursesMenu.is_running
