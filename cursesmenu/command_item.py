import os

from external_item import ExternalItem


class CommandItem(ExternalItem):
    def __init__(self, name, command, menu):
        super(CommandItem, self).__init__(name, menu)
        self.command = command

    def external_action(self):
        os.system(self.command)
