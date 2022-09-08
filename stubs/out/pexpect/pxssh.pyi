from _typeshed import Incomplete
from pexpect import ExceptionPexpect, spawn

class ExceptionPxssh(ExceptionPexpect): ...

class pxssh(spawn):
    name: str
    UNIQUE_PROMPT: str
    PROMPT: Incomplete
    PROMPT_SET_SH: str
    PROMPT_SET_CSH: str
    SSH_OPTS: Incomplete
    force_password: bool
    debug_command_string: Incomplete
    options: Incomplete
    def __init__(
        self,
        timeout: int = ...,
        maxread: int = ...,
        searchwindowsize: Incomplete | None = ...,
        logfile: Incomplete | None = ...,
        cwd: Incomplete | None = ...,
        env: Incomplete | None = ...,
        ignore_sighup: bool = ...,
        echo: bool = ...,
        options=...,
        encoding: Incomplete | None = ...,
        codec_errors: str = ...,
        debug_command_string: bool = ...,
        use_poll: bool = ...,
    ) -> None: ...
    def levenshtein_distance(self, a, b): ...
    def try_read_prompt(self, timeout_multiplier): ...
    def sync_original_prompt(self, sync_multiplier: float = ...): ...
    def login(
        self,
        server,
        username: Incomplete | None = ...,
        password: str = ...,
        terminal_type: str = ...,
        original_prompt: str = ...,
        login_timeout: int = ...,
        port: Incomplete | None = ...,
        auto_prompt_reset: bool = ...,
        ssh_key: Incomplete | None = ...,
        quiet: bool = ...,
        sync_multiplier: int = ...,
        check_local_ip: bool = ...,
        password_regex: str = ...,
        ssh_tunnels=...,
        spawn_local_ssh: bool = ...,
        sync_original_prompt: bool = ...,
        ssh_config: Incomplete | None = ...,
        cmd: str = ...,
    ): ...
    def logout(self) -> None: ...
    def prompt(self, timeout: int = ...): ...
    def set_unique_prompt(self): ...
