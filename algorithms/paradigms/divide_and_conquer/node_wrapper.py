class NodeWrapper:
    def __init__(self, obj, point: tuple):
        self.point = point
        self.obj = obj

    def __lt__(self, other):
        return self.point < other.point

    def __str__(self):
        return "({}, {})".format(self.point, self.obj)
