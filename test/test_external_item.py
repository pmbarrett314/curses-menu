import pytest

from cursesmenu import CursesMenu
from cursesmenu.items import ExternalItem

pytestmark = pytest.mark.usefixtures(
    "mock_cursesmenu_curses",
    "mock_clear",
    "mock_externalitem_curses",
)


@pytest.fixture
def external_items():
    item0 = ExternalItem("item0", should_exit=True)
    item1 = ExternalItem("item1", should_exit=True)
    return [item0, item1]


@pytest.fixture
def menu_with_external_items(external_items):
    menu = CursesMenu("menu", "Test External Items")
    menu.items.append(external_items[0])
    menu.items.append(external_items[1])
    menu.start()
    menu.wait_for_start(timeout=10)
    yield menu
    menu.exit()
    menu.join(timeout=10)


def test_external_item(menu_with_external_items: CursesMenu):
    menu_with_external_items.select()
    menu_with_external_items.join(timeout=10)
    assert not menu_with_external_items.is_alive()
