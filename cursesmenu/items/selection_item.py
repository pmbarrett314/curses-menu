from cursesmenu.items import MenuItem


class SelectionItem(MenuItem):
    def action(self):
        self.menu.exit()
