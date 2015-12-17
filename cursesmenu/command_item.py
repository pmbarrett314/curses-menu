import subprocess
from cursesmenu.external_item import ExternalItem


class CommandItem(ExternalItem):
    def __init__(self, name, command, menu):
        super(CommandItem, self).__init__(name, menu)
        self.command = command
        self.status = 0

    def external_action(self):
        completed_process = subprocess.run(self.command, shell=True)
        self.status = completed_process.returncode
        return self.status
