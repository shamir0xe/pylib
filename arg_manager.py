import sys


class Manager:
    """
    managing arguments
    """
    def __init__(self, begin_idx=1):
        self.args = sys.argv
        self.counter = begin_idx

    def size(self):
        return len(self.args)

    def next_arg(self):
        if self.counter >= self.size():
            return None
        out = self.args[self.counter]
        self.counter += 1
        return out
