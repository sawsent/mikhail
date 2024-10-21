class PathBuilder:
    def __init__(self, starting_path='', sep='/'):
        self.path = starting_path 
        self.sep = sep
    
    def __add__(self, sub_path):
        self.path += self.sep + sub_path
        return self

    def toPath(self):
        return self.path

def build_path(*args, sep='/'):
    return sep.join(args)
