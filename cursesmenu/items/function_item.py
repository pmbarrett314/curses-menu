from cursesmenu.items import ExternalItem


class FunctionItem(ExternalItem):
    def __init__(self, name, menu, function, args=None, kwargs=None, should_exit=False):
        super().__init__(name, menu, should_exit)
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

    def external_action(self):
        self.returned = self.function(*self.args, **self.kwargs)
        return self.returned
