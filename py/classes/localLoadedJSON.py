class localLoadedJSON:
    def __init__(self, relative_path):
        with open(relative_path) as fp:
            self.data = json.load(fp)

    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)