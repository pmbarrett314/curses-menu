import subprocess

from cursesmenu.items import ExternalItem


class CommandItem(ExternalItem):
    """
    A menu item to execute a console command
    """

    def __init__(self, name, menu, command, arguments=None, should_exit=False):
        """
        :type name: str
        :type menu: cursesmenu.CursesMenu

        :param str command: The console command to be executed
        :param list[str] arguments: String arguments to be passed to the command
        :ivar int self.status: the exit status of the command, None if it hasn't been run yet
        """
        super(CommandItem, self).__init__(name, menu, should_exit)
        self.command = command
        if arguments:
            self.arguments = arguments
        else:
            self.arguments = []
        self.status = None

    def external_action(self):
        """
        Runs the command

        :return: the exit status of the command process
        """
        completed_process = subprocess.run(self.command + " " + " ".join(self.arguments), shell=True)
        self.status = completed_process.returncode
        return self.status
