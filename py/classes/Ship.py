class Ship:
    def __init__(self, mod, name, included, weight ):
        self.mod = mod
        self.name = name
        self.included = included
        self.weight = weight
    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)