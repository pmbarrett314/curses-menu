from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import SubmenuItem


class TestSubmenuItem(BaseTestCase):
    def test_init(self):
        root_menu = CursesMenu("root_menu", "test_init")
        submenu1 = CursesMenu("submenu1", "test_init")
        submenu2 = CursesMenu("submenu2", "test_init")
        menu_item_1 = SubmenuItem("menu_item_1", root_menu, submenu1)
        menu_item_2 = SubmenuItem("menu_item_2", root_menu, submenu2, True)
        menu_item_3 = SubmenuItem(name="menu_item_3", menu=root_menu, submenu=submenu2, should_exit=False)
        self.assertEqual(menu_item_1.name, "menu_item_1")
        self.assertEqual(menu_item_2.name, "menu_item_2")
        self.assertEqual(menu_item_3.name, "menu_item_3")
        self.assertEqual(menu_item_1.menu, root_menu)
        self.assertEqual(menu_item_2.menu, root_menu)
        self.assertEqual(menu_item_3.menu, root_menu)
        self.assertFalse(menu_item_1.should_exit)
        self.assertTrue(menu_item_2.should_exit)
        self.assertFalse(menu_item_3.should_exit)
        self.assertEqual(menu_item_1.submenu, submenu1)
        self.assertEqual(menu_item_2.submenu, submenu2)
        self.assertEqual(menu_item_3.submenu, submenu2)
        self.assertEqual(menu_item_1.submenu.parent, root_menu)
        self.assertEqual(menu_item_2.submenu.parent, root_menu)
        self.assertEqual(menu_item_3.submenu.parent, root_menu)

    def test_action(self):
        root_menu = CursesMenu("root_menu", "test_action")
        submenu1 = CursesMenu("submenu1", "test_action")
        submenu2 = CursesMenu("submenu2", "test_action")
        submenu_item_1 = SubmenuItem("submenu_item_1", root_menu, submenu1)
        submenu_item_2 = SubmenuItem("submenu_item_2", root_menu, submenu2)

        root_menu.append_item(submenu_item_1)
        root_menu.append_item(submenu_item_2)

        root_menu.start()
        self.assertIs(CursesMenu.currently_active_menu, root_menu)
        submenu_item_1.action()
        self.assertIs(CursesMenu.currently_active_menu, submenu1)
        CursesMenu.currently_active_menu.exit()
        submenu1.join(timeout=10)
        self.assertIs(CursesMenu.currently_active_menu, root_menu)
        submenu_item_2.action()
        self.assertIs(CursesMenu.currently_active_menu, submenu2)
