import cursesmenu.curses_menu


def main():
    menu = cursesmenu.curses_menu.CursesMenu("Test Menu")
    menu.show()


if __name__ == "__main__":
    main()
