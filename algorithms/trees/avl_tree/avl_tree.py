from .avl_node import AvlNode


class AvlTree:
    def __init__(self):
        self.root = None

    def empty(self):
        return self.root is None

    def insert(self, value):
        self.root = self.__insert(self.root, value)

    def __insert(self, node, value):
        if node is None:
            return AvlNode(value)
        if value < node.value:
            node.left = self.__insert(node.left, value)
        else:
            node.right = self.__insert(node.right, value)

        node.update_height()
        balance_factor = node.get_balance_factor()

        if balance_factor > 1:
            if value < node.left.value:
                return node.rotate_right()
            else:
                node.left = node.left.rotate_left()
                return node.rotate_right()

        if balance_factor < -1:
            if value > node.right.value:
                return node.rotate_left()
            else:
                node.right = node.right.rotate_right()
                return node.rotate_left()

        return node

    def find(self, objective):
        return self.__find(objective, self.root)

    def __find(self, objective, node):
        if node is None or node.value == objective:
            return node
        if objective < node.value:
            return self.__find(objective, node.left)
        return self.__find(objective, node.right)

    def remove(self, objective):
        self.root = self.__remove(objective, self.root)

    def __remove(self, objective, node):
        if node is None:
            return node
        if objective < node.value:
            node.left = self.__remove(objective, node.left)
        elif objective > node.value:
            node.right = self.__remove(objective, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_node = self.__find_minimum(node.right)
            node.value = min_node.value
            node.right = self.__remove(min_node.value, node.right)

        node.update_height()
        balance_factor = node.get_balance_factor()

        if balance_factor > 1:
            if node.left.get_balance_factor() >= 0:
                return node.rotate_right()
            else:
                node.left = node.left.rotate_left()
                return node.rotate_right()

        if balance_factor < -1:
            if node.right.get_balance_factor() <= 0:
                return node.rotate_left()
            else:
                node.right = node.right.rotate_right()
                return node.rotate_left()

        return node

    def __find_minimum(self, node):
        if node.left is None:
            return node
        return self.__find_minimum(node.left)

    def get_size(self):
        return self.__get_size(self.root)

    def __get_size(self, node):
        if node is None:
            return 0
        return self.__get_size(node.left) + 1 + self.__get_size(node.right)

    def get_lowest(self):
        return self.__find_minimum(self.root) if self.root else None

    def get_highest(self):
        return self.__find_maximum(self.root) if self.root else None

    def __find_maximum(self, node):
        if node.right is None:
            return node
        return self.__find_maximum(node.right)

    def inorder_list(self):
        res = []
        self.__inorder_list(self.root, res)
        return res

    def __inorder_list(self, node, res):
        if node is None:
            return
        self.__inorder_list(node.left, res)
        res.append(str(node.value))
        self.__inorder_list(node.right, res)

    def __repr__(self):
        return str(self.inorder_list())
