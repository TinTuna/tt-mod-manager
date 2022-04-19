class Mod:
    def __init__(self, name, author, filesTouched):
        self.name = name
        self.author = author
        self.filesTouched = filesTouched
    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)