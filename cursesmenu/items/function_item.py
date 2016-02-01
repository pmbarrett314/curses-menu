from cursesmenu.items import ExternalItem


class FunctionItem(ExternalItem):
    """
    A menu item to call a Python function
    """

    def __init__(self, name, menu, function, args=None, kwargs=None, should_exit=False):
        """
        :type name: str
        :type menu: cursesemnu.CursesMenu

        :param function: The function to be called
        :param list args: The list of args to be passed to the function
        :param dict kwargs: The dictionary of kwargs to be passed to the function

        :ivar self.returned: the value returned by the function
        """
        super(FunctionItem, self).__init__(name, menu, should_exit)
        if args is not None:
            self.args = args
        else:
            self.args = []
        if kwargs is not None:
            self.kwargs = kwargs
        else:
            self.kwargs = {}
        self.function = function
        self.returned = None

    def action(self):
        """
        Call the function with the given args and kwargs

        :return: the return value of the function
        """
        self.returned = self.function(*self.args, **self.kwargs)
        return self.returned
