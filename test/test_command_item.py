import pathlib
import sys

import pytest

from cursesmenu.items import CommandItem

pytestmark = pytest.mark.usefixtures(
    "mock_cursesmenu_curses",
    "mock_clear",
    "mock_externalitem_curses",
)

test_file_path = pathlib.Path("test.txt")


@pytest.fixture
def create_item():
    return CommandItem(
        "create_item",
        "echo",
        arguments=["hello"],
        stdout_filepath=test_file_path,
    )


@pytest.fixture
def delete_item():
    if sys.platform.startswith(
        "win",
    ):  # pragma: no cover macos # pragma: no cover linux
        return CommandItem("delete_item", "del", arguments=[f"{str(test_file_path)}"])
    else:  # pragma: no cover windows
        return CommandItem("delete_item", f"rm -f {str(test_file_path)}")


@pytest.fixture
def exit_item():
    return CommandItem("return_command_item", "exit", arguments=["42"])


def test_init():
    item1 = CommandItem("return_command_item", "exit", arguments=["42"])
    item2 = CommandItem("return_command_item", "exit 42")
    assert item1.command == "exit"
    assert item2.command == "exit 42"


def test_return(exit_item: CommandItem):
    exit_item.action()

    assert exit_item.get_return() == 42


def test_create(create_item: CommandItem, delete_item: CommandItem):
    create_item.action()
    assert create_item.get_return() == 0
    assert test_file_path.is_file()
    with open(test_file_path, "r") as f:
        assert f.read().strip() == "hello"
    delete_item.action()
    assert delete_item.get_return() == 0
    assert not test_file_path.exists()
