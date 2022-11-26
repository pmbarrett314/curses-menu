import os
import pathlib
import sys
from typing import Generator, List

import pexpect
import pexpect.popen_spawn
import pyte
import pytest

TEST_DIR_PATH = pathlib.Path(__file__).parent.absolute()
BASIC_MENU_PATH = TEST_DIR_PATH.joinpath("example_menus", "basic_menu.py")
ITEM_MENU_PATH = TEST_DIR_PATH.joinpath("example_menus", "menu_with_items.py")

on_bad_platform = sys.platform.startswith("win") or (
    "PYCHARM_HOSTED" in os.environ and "TOX_WORK_DIR" not in os.environ
)


@pytest.mark.skipif(
    on_bad_platform,
    reason="Screen capture doesn't work on Windows",
)
class MenuTester:  # pragma: no-cover-windows
    def su(self, rows: int, cols: int, filepath: pathlib.Path):
        self.rows = rows
        self.cols = cols
        self.screen = pyte.Screen(self.cols, self.rows)
        self.stream = pyte.Stream(self.screen)
        self.filepath = filepath
        self.shell_command = f"python {self.filepath}"

    @property
    def bottom_row(self):
        return "m" + ("q" * (self.cols - 2)) + "j"

    def spawn_process(self, cmd: str, args: List[str]):
        env = os.environ.copy()
        env.update({"LINES": str(self.rows), "COLUMNS": str(self.cols)})
        if not sys.platform.startswith("win32"):
            return pexpect.spawn(
                cmd,
                args,
                echo=False,
                encoding="utf-8",
                dimensions=(self.rows, self.cols),
                env=env,
            )
        else:  # pragma: no cover all
            # this currently doesn't work on windows but I'm keeping this around
            # in case I decide to have another go at it later
            cmd = "{} {}".format(cmd, " ".join(args))
            return pexpect.popen_spawn.PopenSpawn(cmd, encoding="utf-8", env=env)

    def emulate_ansi_terminal(self, raw_output: str, *, clean=True):
        if raw_output in [pexpect.EOF, pexpect.TIMEOUT]:  # pragma: no cover all
            return ""
        self.stream.feed(raw_output)

        lines: List[str] | Generator[str, None, None] = self.screen.display
        self.screen.reset()

        if clean:  # pragma: no cover all
            lines = (line.rstrip() for line in lines)
            lines = (line for line in lines if line)
        lines = list(lines)
        return "\n".join(lines) + "\n"


class TestBasicMenu(MenuTester):  # pragma: no-cover-windows
    def setup_method(
        self,
        _,
        rows=10,
        cols=40,
        filepath=BASIC_MENU_PATH,
    ):
        super().su(rows, cols, filepath)

    def test_basic_menu(self):
        child = self.spawn_process(self.shell_command, [])
        child.expect([self.bottom_row, pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        out = self.emulate_ansi_terminal(child.before) + self.emulate_ansi_terminal(
            child.after,
        )

        with TEST_DIR_PATH.joinpath("menu_data", "basic-menu-screen-0").open(
            "r",
        ) as infile:
            assert infile.read().strip() == out.strip()
        child.sendline()

        child.expect(pexpect.EOF, timeout=5)


class TestMenuWithItems(MenuTester):  # pragma: no-cover-windows
    def setup_method(
        self,
        method,
        rows=10,
        cols=40,
        filepath=ITEM_MENU_PATH,
    ):
        super().su(rows, cols, filepath)

    def test_basic_menu(self):
        child = self.spawn_process(self.shell_command, [])
        child.expect([self.bottom_row, pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        out = self.emulate_ansi_terminal(child.before) + self.emulate_ansi_terminal(
            child.after,
        )

        with TEST_DIR_PATH.joinpath("menu_data", "menu_with_items-0").open(
            "r",
        ) as infile:
            assert infile.read().strip() == out.strip()
        child.sendline()
        child.expect(pexpect.EOF, timeout=5)


if __name__ == "__main__":
    pytest.main()
