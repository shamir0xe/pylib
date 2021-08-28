from .utils import (HashGenerator)

class Node:
	def __init__(self, objective=None):
		self.__value = objective
		self.__height = 1
		self.__size = 1
		self.__parent = self.__left = self.__right = None
		self.__hash = HashGenerator().generate(5)

	def set_value(self, value):
		self.__value = value

	def set_right(self, node):
		if not node is None:
			node.set_par(self)
		self.__right = node

	def set_left(self, node):
		if not node is None:
			node.set_par(self)
		self.__left = node

	def set_par(self, node):
		self.__parent = node

	def set_hash(self, node_hash):
		self.__hash = node_hash

	def get_balance(self):
		left_height = 0
		if not self.__left is None:
			left_height = self.__left.get_height()
		right_height = 0
		if not self.__right is None:
			right_height = self.__right.get_height()
		return left_height - right_height

	def get_left(self):
		return self.__left

	def get_right(self):
		return self.__right

	def get_value(self):
		return self.__value

	def get_hash(self):
		return self.__hash

	def get_size(self):
		return self.__size

	def __str__(self):
		return "val: [{}], par: [{}], sz: [{}], h: [{}], hash: [{}]".format(
			self.__value, self.__parent, self.__size, self.__height, self.__hash)

	def get_height(self):
		if self.__value is None:
			return 0
		return self.__height

	def update_height(self):
		self.__height = 1
		maxi = 0
		if self.__left:
			maxi = max(maxi, self.__left.get_height())
		if self.__right:
			maxi = max(maxi, self.__right.get_height())
		self.__height += maxi

	def update_size(self):
		self.__size = 1
		if self.__left:
			self.__size += self.__left.get_size()
		if self.__right:
			self.__size += self.__right.get_size()

	def update(self):
		self.update_height()
		self.update_size()

	def __eq__(self, other):
		if self.__value == other.get_value():
			return self.__hash == other.get_hash()
		return False

	def __lt__(self, other):
		# if other is None:
		# 	return False
		# if self.__value == other.get_value():
		# 	return False
		# if other.get_value is None:
		# 	return False
		return self.__value < other.get_value()
