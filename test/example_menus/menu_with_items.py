import cursesmenu
from cursesmenu.items import MenuItem


def main():
    menu = cursesmenu.CursesMenu("Test Menu")
    menu.items.append(MenuItem("item1", should_exit=True))
    menu.items.append(MenuItem("item2", should_exit=True))
    menu.show()


if __name__ == "__main__":
    main()
