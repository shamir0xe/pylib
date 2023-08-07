from .avl_node import AvlNode


class AvlTree:
    """
    implementation of the avl-tree
    all of the orders are optimum as hell
    node's value should have been implemented with __lt__ operator
    """

    def __init__(self):
        self.__root = None

    def get_root(self):
        """
        returns the current root of the tree
        """
        return self.__root

    def empty(self):
        return self.__root is None

    def insert(self, value):
        """
        adding a new node with a value equals to {value}
        """
        if self.get_root() is None:
            self.__root = AvlNode(value)
        else:
            self.__root = self.__add(self.__root, AvlNode(value))

    def find(self, objective):
        """
        returns the node with a value equals to {objective}
        """
        return self.__find(objective, self.__root)

    def find_node(self, node):
        """
        check whether the node is exist or not
        """
        # debug_text("finding node with value = {}".format(node.get_value()))
        # debug_text("node = {}".format(node))
        return self.__find(node.get_value(), self.__root, node.get_hash())

    def remove(self, objective):
        """
        removes the node with a value equals to {objective}"""
        node = self.find(objective)
        if node is None:
            return False
        self.__root = self.__remove(objective, self.__root)
        return True

    def remove_node(self, node):
        """
        removes the node with it's actual node
        """
        # debug_text("going to remove the node with {} as value".format(node.get_value()))
        node = self.find_node(node)
        if node is None:
            return False
        # debug_text("\n\n==>{}".format(node.get_hash()))
        self.__root = self.__remove(node.get_value(), self.__root, node.get_hash())
        return True

    def get_size(self):
        if self.__root is None:
            return 0
        return self.__root.get_size()

    def get_lowest(self):
        """
        returns the node with the lowest value in the tree
        """
        if self.__root is None:
            return None
        node = self.__root
        while not node.get_left() is None:
            node = node.get_left()
        return node

    def get_highest(self):
        """
        returns the node with the highest value in the tree
        """
        if self.__root is None:
            return None
        node = self.__root
        while not node.get_right() is None:
            node = node.get_right()
        return node

    def inorder_list(self, node, res):
        """
        returns the inorder list of the tree as array of string
        """
        if node is None:
            return
        res.append("(")
        self.inorder_list(node.get_left(), res)
        res.append(",")
        if node.get_value():
            res.append(str(node.get_value()))
            # res.append(node.get_hash())
        res.append(",")
        self.inorder_list(node.get_right(), res)
        res.append(")")

    def __remove(self, objective, node, node_hash=None):
        if node is None:
            return None
        if objective < node.get_value():
            left = self.__remove(objective, node.get_left(), node_hash)
            node.set_left(left)
        elif node.get_value() < objective:
            right = self.__remove(objective, node.get_right(), node_hash)
            node.set_right(right)
        else:
            if node_hash is None or node.get_hash() == node_hash:
                right = node.get_right()
                if not right is None:
                    node = self.__rotate_left(node)
                    left = self.__remove(
                        objective, node.get_left(), node.get_left().get_hash()
                    )
                    node.set_left(left)
                else:
                    left = node.get_left()
                    if not left is None:
                        node = self.__rotate_right(node)
                        right = self.__remove(
                            objective, node.get_right(), node.get_right().get_hash()
                        )
                        node.set_right(right)
                    else:
                        del node
                        return None
            else:
                right = self.__remove(objective, node.get_right(), node_hash)
                node.set_right(right)
        res = self.__relax(node)
        res.set_par(None)
        return res

    def __find(self, objective, node, node_hash=None):
        if node is None:
            return None

        c = "=="
        if objective < node.get_value():
            c = "<"
        if node.get_value() < objective:
            c = ">"
        # debug_text("obj{}node - {}/{}".format(c, node.get_hash(), node_hash))
        if objective < node.get_value():
            return self.__find(objective, node.get_left(), node_hash)
        if node.get_value() < objective:
            return self.__find(objective, node.get_right(), node_hash)
        if node_hash is None or node.get_hash() == node_hash:
            # debug_text("c'mon")
            return node
        return self.__find(objective, node.get_right(), node_hash)

    def __add(self, cur, node):
        if node < cur:
            if cur.get_left() is None:
                cur.set_left(node)
                node.set_par(cur)
            else:
                left = self.__add(cur.get_left(), node)
                left.set_par(cur)
                cur.set_left(left)
        else:
            if cur.get_right() is None:
                cur.set_right(node)
                node.set_par(cur)
            else:
                right = self.__add(cur.get_right(), node)
                right.set_par(cur)
                cur.set_right(right)
        return self.__relax(cur)

    def __get_height(self, node):
        if node is None:
            return 0
        return node.get_height()

    def __relax(self, node):
        if node is None:
            return
        node.update()
        balance = node.get_balance()
        if balance > 1:
            left_left = node.get_left().get_left()
            left_right = node.get_left().get_right()
            if self.__get_height(left_left) <= self.__get_height(left_right):
                node.set_left(self.__rotate_left(node.get_left()))
            return self.__rotate_right(node)
        elif balance < -1:
            right_right = node.get_right().get_right()
            right_left = node.get_right().get_left()
            if self.__get_height(right_right) <= self.__get_height(right_left):
                node.set_right(self.__rotate_right(node.get_right()))
            return self.__rotate_left(node)
        return node

    def __rotate_right(self, y):
        x = y.get_left()
        t_2 = x.get_right()
        x.set_right(y)
        y.set_left(t_2)
        y.update()
        x.update()
        x.set_par(None)
        return x

    def __rotate_left(self, x):
        y = x.get_right()
        t_2 = y.get_left()
        y.set_left(x)
        x.set_right(t_2)
        x.update()
        y.update()
        y.set_par(None)
        return y

    def __str__(self):
        res = []
        self.inorder_list(self.__root, res)
        list_string = "".join(res)
        return "list: {}\nbalance: {}, size: {}".format(
            list_string, self.__root.get_balance(), self.__root.get_size()
        )
