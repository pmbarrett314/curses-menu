from typing import Optional

from _typeshed import Incomplete
from pyte import Screen

class Stream:
    basic: Incomplete
    escape: Incomplete
    sharp: Incomplete
    csi: Incomplete
    events: Incomplete
    listener: Incomplete
    strict: Incomplete
    use_utf8: bool

    def __init__(self, screen: Optional[Screen] = ..., strict: bool = ...) -> None: ...
    def attach(self, screen: Screen) -> None: ...
    def detach(self, screen) -> None: ...
    def feed(self, data: str) -> None: ...
    def select_other_charset(self, code) -> None: ...

class ByteStream(Stream):
    utf8_decoder: Incomplete

    def __init__(self, *args, **kwargs) -> None: ...
    def feed(self, data) -> None: ...

    use_utf8: bool

    def select_other_charset(self, code) -> None: ...
