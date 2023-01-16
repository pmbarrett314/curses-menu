from _typeshed import Incomplete

from .spawnbase import SpawnBase

class fdspawn(SpawnBase):
    args: Incomplete
    command: Incomplete
    child_fd: Incomplete
    own_fd: bool
    closed: bool
    name: Incomplete
    use_poll: Incomplete
    def __init__(
        self,
        fd,
        args: Incomplete | None = ...,
        timeout: int = ...,
        maxread: int = ...,
        searchwindowsize: Incomplete | None = ...,
        logfile: Incomplete | None = ...,
        encoding: Incomplete | None = ...,
        codec_errors: str = ...,
        use_poll: bool = ...,
    ) -> None: ...
    def close(self) -> None: ...
    def isalive(self): ...
    def terminate(self, force: bool = ...) -> None: ...
    def send(self, s): ...
    def sendline(self, s): ...
    def write(self, s) -> None: ...
    def writelines(self, sequence) -> None: ...
    def read_nonblocking(self, size: int = ..., timeout: Incomplete = ...): ...
