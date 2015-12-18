import unittest
from unittest.mock import Mock, patch
import curses


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_curses = Mock(spec=curses)
        self.mock_window = Mock(spec=['keypad', 'addstr', 'border', 'getch', 'refresh', 'clear'])
        self.mock_window.getch.return_value = ord('a')
        self.mock_curses.initscr.return_value = self.mock_window
        self.patcher = patch(target='cursesmenu.curses_menu.curses', new=self.mock_curses)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
