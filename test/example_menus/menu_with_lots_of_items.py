import cursesmenu
from cursesmenu.items import MenuItem


def main():
    menu = cursesmenu.CursesMenu("Test Menu", "subtitle")
    for i in range(100):
        menu.items.append(MenuItem(f"item{i}", should_exit=True))  # noqa: PERF401
    menu.show()


if __name__ == "__main__":
    main()
