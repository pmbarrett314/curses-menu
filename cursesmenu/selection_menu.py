from cursesmenu import CursesMenu
from cursesmenu.items import SelectionItem


class SelectionMenu(CursesMenu):
    """
    A menu that simplifies item creation, just give it a list of strings and it builds the menu for you
    """

    def __init__(self, strings, title=None, subtitle=None, show_exit_option=True):
        """
        :ivar list[str] strings: The list of strings this menu should be built from
        """
        super(SelectionMenu, self).__init__(title, subtitle, show_exit_option)
        for index, item in enumerate(strings):
            self.append_item(SelectionItem(item, index, self))

    @classmethod
    def get_selection(cls, strings, title="Select an option", subtitle=None, exit_option=True, _menu=None):
        """
        Single-method way of getting a selection out of a list of strings

        :param list[str] strings: the list of string used to build the menu
        :param list _menu: should probably only be used for testing, pass in a list and the created menu used \
        internally by the method will be appended to it
        """
        menu = cls(strings, title, subtitle, exit_option)
        if _menu is not None:
            _menu.append(menu)
        menu.show()
        menu.join()
        return menu.selected_option

    def append_string(self, string):
        self.append_item(SelectionItem(string))
