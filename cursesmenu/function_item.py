from external_item import ExternalItem


class FunctionItem(ExternalItem):
    def __init__(self, name, function, menu=None):
        super(FunctionItem, self).__init__(name, menu)
        self.function = function

    def external_action(self):
        self.function()
