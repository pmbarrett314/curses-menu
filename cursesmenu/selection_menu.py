from cursesmenu import CursesMenu
from cursesmenu.items import SelectionItem


class SelectionMenu(CursesMenu):
    """
    A menu that simplifies item creation, just give it a list of strings and it builds the menu for you
    """

    def __init__(self, strings, title=None, subtitle=None, show_exit_option=True):
        """
        :param strings: The list of strings this menu should be built from
        :type title: str
        :type subtitle: str
        :type strings: list[str]
        :type show_exit_option: bool
        :type parent: CursesMenu
        """
        super(SelectionMenu, self).__init__(title, subtitle, show_exit_option)
        for index, item in enumerate(strings):
            self.append_item(SelectionItem(item, index, self))

    @classmethod
    def get_selection(cls, strings, title="Select an option", subtitle=None, exit_option=True, _menu=[]):
        """
        Simplifies everything even further. Just give this method a list of strings, and it will show the menu and
        return the selected index

        :type title: str
        :type subtitle: str
        :type strings: list[str]
        :type exit_option: bool
        :type parent: CursesMenu
        :return: the selected index
        :rtype: int
        """
        menu = cls(strings, title, subtitle, exit_option)
        _menu.append(menu)
        menu.show()
        menu.join()
        return menu.selected_option
