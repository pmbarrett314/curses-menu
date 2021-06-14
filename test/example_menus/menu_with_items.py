import cursesmenu
from cursesmenu.items import MenuItem


def main():
    menu = cursesmenu.CursesMenu("Test Menu")
    menu.append_item(MenuItem("item1", should_exit=True))
    menu.append_item(MenuItem("item2", should_exit=True))
    menu.show()


if __name__ == "__main__":
    main()
