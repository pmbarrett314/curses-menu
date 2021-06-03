import curses
from threading import Thread

import unittest

from unittest.mock import Mock, patch


class ThreadedReturnGetter(Thread):
    def __init__(self, function, args=None, kwargs=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.return_value = None
        self.function = function
        try:
            super(ThreadedReturnGetter, self).__init__(target=self.get_return_value,
                                                       args=args, kwargs=kwargs,
                                                       daemon=True)
        except TypeError:
            super(ThreadedReturnGetter, self).__init__(target=self.get_return_value,
                                                       args=args, kwargs=kwargs)
            self.daemon = True

    def get_return_value(self, *args, **kwargs):
        self.return_value = self.function(*args, **kwargs)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_curses = Mock(spec=curses)
        self.mock_window = Mock(
            spec=['keypad', 'addstr', 'border', 'getch', 'refresh', 'clear',
                  'getmaxyx'])
        self.mock_window.getch.return_value = ord('a')
        self.mock_window.getmaxyx.return_value = (999999999, 999999999)
        self.mock_curses.initscr.return_value = self.mock_window
        self.mock_curses.wrapper.side_effect = lambda x: x(self.mock_window)

        self.patcher = patch(target='cursesmenu.curses_menu.curses',
                             new=self.mock_curses)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
