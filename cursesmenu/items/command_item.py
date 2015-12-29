import subprocess

from cursesmenu.items import ExternalItem


class CommandItem(ExternalItem):
    """
    A menu item to execute a console command
    """

    def __init__(self, name, menu, command, should_exit=False):
        """
        :type name: str
        :type menu: cursesmenu.CursesMenu

        :param str command: The console command to be executed
        """
        super().__init__(name, menu, should_exit)
        self.command = command
        self.status = 0

    def external_action(self):
        """
        Runs the command

        :return: the exit status of the command process
        """
        completed_process = subprocess.run(self.command, shell=True)
        self.status = completed_process.returncode
        return self.status
