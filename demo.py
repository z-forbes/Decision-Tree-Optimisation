from Node import *
from Tree import * 
from algos import *
from utils import *

print("Here is a simple tree:")
root = Node(1)
n2 = Node(2, root, False)
n3 = Node(3, root, True)
Node(True, n2, False)
Node(False, n2, True)
Node(False, n3, True)
Node(True, n3, False)
tree = Tree(root)
print(tree)


print("\nThe tree class has some helpful methods:")
print("Root: {}".format(tree.root))
print("Depth: {}".format(tree.depth))
print("Size: {}".format(tree.nodes_amount))


print("\nHere is a simple truth table:")
# each row is [f, x1, ... , xn] despite being displayed differently
tt = [[0, 1, 0, 1], [1, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 1], [0, 0, 0, 0]]
# tt = tt_gen(3,5) # uncomment to generate a random truth table
print_tt(tt)


print("\nTrees can be generated from truth tables using the algorithms in algos.py:")
trees = []
trees.append(optimal(tt))
# trees.append(id3(tt))
# trees.append(c45(tt))
# trees.append(cart(tt))
# trees.append(double_id3(tt))
trees.append(topdown(tt)) # the worst-case algorithm

for t in trees:
    assert verify(t, tt)
    print(t, "\n")


print("\nalgos.py has some useful functions beyond tree construction:")
print("The truth table above has...")

print("   -{} distinct trees.".format(count_trees(tt)))
assert count_trees(tt)==len(gen_trees(tt))

print("   -{} distinct optimal trees.".format(len(gen_optimal(tt))))

