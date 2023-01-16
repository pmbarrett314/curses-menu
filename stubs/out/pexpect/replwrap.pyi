from _typeshed import Incomplete

PY3: Incomplete
basestring = str
PEXPECT_PROMPT: str
PEXPECT_CONTINUATION_PROMPT: str

class REPLWrapper:
    child: Incomplete
    prompt: Incomplete
    continuation_prompt: Incomplete
    def __init__(
        self,
        cmd_or_spawn,
        orig_prompt,
        prompt_change,
        new_prompt=...,
        continuation_prompt=...,
        extra_init_cmd: Incomplete | None = ...,
    ) -> None: ...
    def set_prompt(self, orig_prompt, prompt_change) -> None: ...
    def run_command(self, command, timeout: int = ..., async_: bool = ...): ...

def python(command: str = ...): ...
def bash(command: str = ...): ...
