class Node:
    def __str__(self):
        to_format = ""
        if self.is_leaf():
            return " {}".format(str(self.value)[0])
        else:
            return "x{}".format(self.value)
        
    def __init__(self, value, parent=None, path=None):
        self.depth = 1                         # depth of node
        self.value = value                     # bool if leaf, int if node
        self.parent = self.set_parent(parent)  # node 
        self.children = []                     # nodes
        self.path = path                       # T/F of parent path

        # used when printing tree
        ######
        self.left = None
        self.right = None
        ######
    
    def set_parent(self, p_node):
    # if node is root
        if p_node==None:
            return None
        
        p_node.children.append(self)
        self.depth = (p_node.depth)+1
        return p_node
    
    def is_root(self):
        return self.parent == None
    
    def is_leaf(self):
        return isinstance(self.value, bool)

    # PRINTS A STRING CONTAINING INFO ABOUT THE NODE
    def print_info(self):
        output = ""
        if self.is_root():
            output += "ROOT NODE x"
        elif self.is_leaf():
            output += "LEAF "
        else:
            output += "NODE: x"
        output += str(self.value)
        output += "\nparent: " + str(self.parent)
        output += "\nparent path: " + str(self.path)
        output += "\nchildren: " + str([str(c) for c in self.children])
        print(output)

    # turns True into T and False into F where applicable
    def pretty_value(self):
        if self.is_leaf():
            return str(self.value)[0] 
        else:
            return self.value
    
    # CONVERTS Tree(self) TO STRING
    # code stolen from https://bit.ly/3i7ZVw3
    def tree_to_string(self):
        lines, *_ = self._display_aux()
        output = ""
        for line in lines:
            output += line + "\n"
        return output[:len(output)-1] #-1 removes extra line

    # should really be called _tree_to_string_aux(self)
    def _display_aux(self):
        kid_n = len(self.children)
        if kid_n != 0 and kid_n !=2:
            raise Exception("Node: {} has {} children".format(self, kid_n))
        
        if kid_n == 2:
            self.left = self.children[0]
            self.right = self.children[1]
        # else: self.children = [None, None] since default
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.pretty_value()
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.pretty_value()
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.pretty_value()
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.pretty_value()
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2