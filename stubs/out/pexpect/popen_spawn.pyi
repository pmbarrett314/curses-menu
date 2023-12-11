from _typeshed import Incomplete

from .exceptions import EOF as EOF
from .spawnbase import PY3 as PY3
from .spawnbase import SpawnBase as SpawnBase
from .utils import string_types as string_types

class PopenSpawn(SpawnBase):
    crlf: Incomplete
    proc: Incomplete
    pid: Incomplete
    closed: bool
    def __init__(
        self,
        cmd,
        timeout: int = ...,
        maxread: int = ...,
        searchwindowsize: Incomplete | None = ...,
        logfile: Incomplete | None = ...,
        cwd: Incomplete | None = ...,
        env: Incomplete | None = ...,
        encoding: Incomplete | None = ...,
        codec_errors: str = ...,
        preexec_fn: Incomplete | None = ...,
    ) -> None: ...
    flag_eof: bool

    def read_nonblocking(self, size, timeout): ... # pyright: ignore [reportIncompatibleMethodOverride]
    def write(self, s) -> None: ...
    def writelines(self, sequence) -> None: ...
    def send(self, s): ...
    def sendline(self, s: str = ...): ...
    exitstatus: Incomplete
    signalstatus: Incomplete
    terminated: bool
    def wait(self): ...
    def kill(self, sig) -> None: ...
    def sendeof(self) -> None: ...
