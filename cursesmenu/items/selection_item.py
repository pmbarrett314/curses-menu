from cursesmenu.items import MenuItem


class SelectionItem(MenuItem):
    """
    The item type used in SelectionMenus. Currently just exits the menu
    """

    def __init__(self, name, menu):
        super().__init__(name, menu, should_exit=True)
