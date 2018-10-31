class Node:

    def __init__(self, is_root, parent, name, is_leaf, left_child = None, right_child = None):
        self.is_root = is_root
        self.parent = parent
        self.name = name
        self.value = None
        self.is_leaf = is_leaf
        self.left_child = left_child
        self.right_child = right_child
        self.calculate_function = ""

    def get_is_root(self):
        return self.is_root

    def set_is_leaf(self, is_leaf):
        self.is_leaf = is_leaf

    def get_is_leaf(self):
        return self.is_leaf

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def set_left_child(self, left_child):
        self.left_child = left_child

    def set_right_child(self, right_child):
        self.right_child = right_child

    def get_left_child(self):
        return self.left_child

    def get_right_child(self):
        return self.right_child

    def set_calculate_function(self, calculate_function):
        self.calculate_function = calculate_function

    def get_calculate_function(self):
        return self.calculate_function

    def calculate(self, func):
        if self.left_child is None:
            return self.value
        if self.right_child is None:
            self.value = func(self.left_child.get_value())
        else:
            self.value = func(self.left_child.get_value(), self.right_child.get_value())

        return self.value

    def to_dict(self):
        dict = {}
        dict["name"] = self.name
        dict["is_root"] = self.is_root
        dict["parent"] = self.parent
        dict["value"] = self.value
        dict["is_leaf"] = self.is_leaf
        if self.left_child is None:
            dict["left_child"] = None
            dict["right_child"] = None
        elif self.right_child is None:
            dict["left_child"] = self.left_child.to_dict()
            dict["right_child"] = None
        else:
            dict["left_child"] = self.left_child.to_dict()
            dict["right_child"] = self.right_child.to_dict()

        return dict

