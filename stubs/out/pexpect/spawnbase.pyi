from typing import Optional

from _typeshed import Incomplete

from .exceptions import EOF as EOF
from .exceptions import TIMEOUT as TIMEOUT
from .exceptions import ExceptionPexpect as ExceptionPexpect
from .expect import Expecter as Expecter
from .expect import searcher_re as searcher_re
from .expect import searcher_string as searcher_string

PY3: Incomplete
text_type: Incomplete

class _NullCoder:
    @staticmethod
    def encode(b, final: bool = ...): ...
    @staticmethod
    def decode(b, final: bool = ...): ...

class SpawnBase:
    encoding: Incomplete
    pid: Incomplete
    flag_eof: Incomplete
    stdin: Incomplete
    stdout: Incomplete
    stderr: Incomplete
    searcher: Incomplete
    ignorecase: bool
    before: Incomplete
    after: Incomplete
    match: Incomplete
    match_index: Incomplete
    terminated: bool
    exitstatus: Incomplete
    signalstatus: Incomplete
    status: Incomplete
    child_fd: int
    timeout: Incomplete
    delimiter: Incomplete
    logfile: Incomplete
    logfile_read: Incomplete
    logfile_send: Incomplete
    maxread: Incomplete
    searchwindowsize: Incomplete
    delaybeforesend: float
    delayafterclose: float
    delayafterterminate: float
    delayafterread: float
    softspace: bool
    name: Incomplete
    closed: bool
    codec_errors: Incomplete
    string_type: Incomplete
    buffer_type: Incomplete
    crlf: bytes
    allowed_string_types: Incomplete
    linesep: Incomplete
    write_to_stdout: Incomplete
    async_pw_transport: Incomplete
    def __init__(
        self,
        timeout: int = ...,
        maxread: int = ...,
        searchwindowsize: Incomplete | None = ...,
        logfile: Incomplete | None = ...,
        encoding: Incomplete | None = ...,
        codec_errors: str = ...,
    ): ...
    buffer: Incomplete
    def read_nonblocking(self, size: int = 1, timeout: Incomplete = None): ...
    def compile_pattern_list(self, patterns): ...
    def expect(
        self,
        pattern,
        timeout: int = ...,
        searchwindowsize: int = ...,
        async_: bool = ...,
        **kw,
    ): ...
    def expect_list(
        self,
        pattern_list,
        timeout: int = ...,
        searchwindowsize: int = ...,
        async_: bool = ...,
        **kw,
    ): ...
    def expect_exact(
        self,
        pattern_list,
        timeout: int = ...,
        searchwindowsize: int = ...,
        async_: bool = ...,
        **kw,
    ): ...
    def expect_loop(
        self, searcher, timeout: int = ..., searchwindowsize: int = ...
    ): ...
    def read(self, size: int = ...): ...
    def readline(self, size: int = ...): ...
    def __iter__(self): ...
    def readlines(self, sizehint: int = ...): ...
    def fileno(self): ...
    def flush(self) -> None: ...
    def isatty(self): ...
    def __enter__(self): ...
    def __exit__(self, etype, evalue, tb) -> None: ...
