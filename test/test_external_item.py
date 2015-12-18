from base_test_case import BaseTestCase
from unittest.mock import patch
from cursesmenu.curses_menu import CursesMenu

class TestExternalItem(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.external_item_patcher = patch(target='cursesmenu.external_item.curses', new=self.mock_curses)
        self.external_item_patcher.start()
        self.addCleanup(self.external_item_patcher.stop)
        self.menu = CursesMenu("Test menu 1", "Subtitle 1")
