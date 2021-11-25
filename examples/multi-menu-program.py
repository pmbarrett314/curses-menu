from cursesmenu import CursesMenu
from cursesmenu.items import MenuItem


def main():
    menu1 = CursesMenu("Menu 1")
    item1 = MenuItem("Item 1", menu1, should_exit=True)
    menu1.items.append(item1)
    menu1.show()
    i = input("Enter some input:")
    menu2 = CursesMenu("Menu 2")
    item2 = MenuItem("Item 2", menu2, should_exit=True)
    menu2.items.append(item2)

    menu2.show()


if __name__ == "__main__":
    main()
