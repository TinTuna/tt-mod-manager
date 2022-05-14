class Mod:
    def __init__(self, name, pathName, author, included, files_touched, clash):
        self.name = name
        self.pathName = pathName
        self.author = author
        self.included = included
        self.files_touched = files_touched
        self.clash = clash
    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)