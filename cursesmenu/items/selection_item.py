from cursesmenu.items import MenuItem


class SelectionItem(MenuItem):
    def __init__(self, name, menu):
        super().__init__(name, menu, should_exit=True)
