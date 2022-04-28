class itemEntry:
    def __init__(self, name, weight, quantity):
        self.name = name
        self.weight = weight
        self.quantity = quantity
    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)