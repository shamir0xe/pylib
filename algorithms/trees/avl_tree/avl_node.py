class AvlNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __lt__(self, other):
        return self.value < other.value

    def update_height(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1

    def get_balance_factor(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

    def rotate_right(self):
        x = self.left
        t_2 = x.right
        x.right = self
        self.left = t_2
        self.update_height()
        x.update_height()
        return x

    def rotate_left(self):
        y = self.right
        t_2 = y.left
        y.left = self
        self.right = t_2
        self.update_height()
        y.update_height()
        return y

    def __repr__(self):
        return str(self.value)

