from cursesmenu import CursesMenu
from cursesmenu.items import SelectionItem


class SelectionMenu(CursesMenu):
    def __init__(self, strings, title=None, subtitle=None, exit_option=True, parent=None):
        super().__init__(title, subtitle, None, exit_option, parent)
        for item in strings:
            self.append_item(SelectionItem(item, self))

    @classmethod
    def get_selection(cls, strings, title="Select an option", subtitle=None, exit_option=True, parent=None):
        menu = cls(strings, title, subtitle, exit_option, parent)
        menu.show()
        return menu.selected_option
