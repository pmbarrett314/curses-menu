from _typeshed import Incomplete

from .exceptions import EOF as EOF
from .exceptions import TIMEOUT as TIMEOUT
from .pty_spawn import spawn as spawn

def run(
    command,
    timeout: int = ...,
    withexitstatus: bool = ...,
    events: Incomplete | None = ...,
    extra_args: Incomplete | None = ...,
    logfile: Incomplete | None = ...,
    cwd: Incomplete | None = ...,
    env: Incomplete | None = ...,
    **kwargs,
): ...
def runu(
    command,
    timeout: int = ...,
    withexitstatus: bool = ...,
    events: Incomplete | None = ...,
    extra_args: Incomplete | None = ...,
    logfile: Incomplete | None = ...,
    cwd: Incomplete | None = ...,
    env: Incomplete | None = ...,
    **kwargs,
): ...
