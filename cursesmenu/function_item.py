from cursesmenu.external_item import ExternalItem


class FunctionItem(ExternalItem):
    def __init__(self, name, function, menu, *args, **kwargs):
        super(FunctionItem, self).__init__(name, menu, )
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.returned = None

    def external_action(self):
        self.returned = self.function(*self.args, **self.kwargs)
        return self.returned
