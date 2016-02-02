from cursesmenu.items import ExternalItem


class FunctionItem(ExternalItem):
    """
    A menu item to call a Python function
    """

    def __init__(self, text, function, args=None, kwargs=None, menu=None, should_exit=False):
        """
        :type text: str
        :type menu: cursesemnu.CursesMenu

        :param function: The function to be called
        :param list args: The list of args to be passed to the function
        :param dict kwargs: The dictionary of kwargs to be passed to the function

        :ivar self.return_value: the value returned by the function
        """
        super(FunctionItem, self).__init__(text=text, menu=menu, should_exit=should_exit)

        self.function = function

        if args is not None:
            self.args = args
        else:
            self.args = []
        if kwargs is not None:
            self.kwargs = kwargs
        else:
            self.kwargs = {}

        self.return_value = None

    def action(self):
        """
        Call the function with the given args and kwargs

        :return: the return value of the function
        """
        self.return_value = self.function(*self.args, **self.kwargs)

    def get_return(self):
        return self.return_value
