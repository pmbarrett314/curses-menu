import subprocess

from cursesmenu.items import ExternalItem


class CommandItem(ExternalItem):
    def __init__(self, name, menu, command, should_exit=False):
        super().__init__(name, menu, should_exit)
        self.command = command
        self.status = 0

    def external_action(self):
        completed_process = subprocess.run(self.command, shell=True)
        self.status = completed_process.returncode
        return self.status
