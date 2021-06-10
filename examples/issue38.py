from cursesmenu import CursesMenu
from cursesmenu.items import ExternalItem


class TestItem(ExternalItem):
    def action(self):
        print("Foo")
        input("press enter")


if __name__ == "__main__":
    menu = CursesMenu()
    menu.append_item(TestItem("this is a test item"))
    menu.show()
