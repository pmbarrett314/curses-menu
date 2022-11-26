import asyncio

from _typeshed import Incomplete
from pexpect import EOF as EOF

async def expect_async(expecter, timeout: Incomplete | None = ...): ...
async def repl_run_command_async(repl, cmdlines, timeout: int = ...): ...

class PatternWaiter(asyncio.Protocol):
    transport: Incomplete
    expecter: Incomplete
    fut: Incomplete
    def set_expecter(self, expecter) -> None: ...
    def found(self, result) -> None: ...
    def error(self, exc) -> None: ...
    def connection_made(self, transport) -> None: ...
    def data_received(self, data) -> None: ...
    def eof_received(self) -> None: ...
    def connection_lost(self, exc) -> None: ...
