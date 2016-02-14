try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import ExternalItem


class TestExternalItem(BaseTestCase):
    def setUp(self):
        super(TestExternalItem, self).setUp()

        self.mock_set_up = MagicMock()
        self.mock_action = MagicMock(return_value=0)
        self.mock_clean_up = MagicMock()
        ExternalItem.set_up = self.mock_set_up
        ExternalItem.clean_up = self.mock_clean_up
        ExternalItem.action = self.mock_action
