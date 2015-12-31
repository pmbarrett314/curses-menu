from unittest.mock import MagicMock

from base_test_case import BaseTestCase
from cursesmenu import CursesMenu
from cursesmenu.items import ExternalItem


class TestExternalItem(BaseTestCase):
    def setUp(self):
        super(TestExternalItem, self).setUp()

        self.mock_set_up = MagicMock()
        self.mock_external = MagicMock(return_value=0)
        self.mock_clean_up = MagicMock()
        ExternalItem._set_up_terminal = self.mock_set_up
        ExternalItem._clean_up_terminal = self.mock_clean_up
        ExternalItem.external_action = self.mock_external

        self.menu = CursesMenu("Test menu 1", "Subtitle 1")

    def test_action(self):
        external_item = ExternalItem("test", self.menu)
        self.assertEqual(external_item.action(), 0)

        self.mock_set_up.assert_any_call()
        self.mock_external.assert_any_call()
        self.mock_clean_up.assert_any_call()
