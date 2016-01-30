import sys
if sys.version_info<(2,7):
    import unittest2 as unittest
else:
    import unittest
    
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
import curses
from threading import Thread


class ThreadedReturnGetter():
    def __init__(self, function, *args, **kwargs):
        self.return_value = None
        self.function = function
        try:
            self.thread = Thread(target=self.get_return_value, args=args, kwargs=kwargs, daemon=True)
        except TypeError:
            self.thread = Thread(target=self.get_return_value, args=args, kwargs=kwargs)
            self.thread.daemon = True

    def start(self):
        self.thread.start()

    def join(self, timeout):
        self.thread.join(timeout=timeout)

    def is_alive(self):
        return self.thread.is_alive()

    def get_return_value(self, *args, **kwargs):
        self.return_value = self.function(*args, **kwargs)


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_curses = Mock(spec=curses)
        self.mock_window = Mock(spec=['keypad', 'addstr', 'border', 'getch', 'refresh', 'clear'])
        self.mock_window.getch.return_value = ord('a')
        self.mock_curses.initscr.return_value = self.mock_window
        self.patcher = patch(target='cursesmenu.curses_menu.curses', new=self.mock_curses)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
