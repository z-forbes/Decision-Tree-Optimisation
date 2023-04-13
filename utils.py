from random import randint
from Tree import *
from Node import *

def tt_valid(tt):
    xs = len(tt[0])
    rs = len(tt)

    if xs<1 or rs<1:
        raise Exception("xs: {}, rs {}".format(rs, xs))
    max_rs = 2**xs
    if rs>(max_rs):
        raise Exception("rs>max_rs ({}>{})".format(rs, max_rs))
    
    return True

def xs_rs_valid(xs, rs):
    output = [None for _ in range(rs)]
    output[0] = [None for _ in range(xs)]
    return tt_valid(output)


# GENERATES A RANDOM TRUTH TABLE OF SPECIFIED SIZE 
def tt_gen(xs, rows):
    xs_rs_valid(xs, rows) # Exception if invalid    
    output = []
    while len(output)<rows:
        new_row = [randint(0,1) for e in range(xs)]
        if new_row in output:
            continue
        else:
            output.append(new_row)
    for c in output:
        c.append(c[0])
        c[0] = randint(0,1)

    return output

def print_tt(ttt):
    tt = [row.copy() for row in ttt] #deep copy
    print([x for x in range(1,len(tt[0]))], end="")
    print(" f")
    for row in tt:
        if len(tt[0])>10:
            row[10:] = [str(e)+"." for e in row[10:]]
        line = str(row[1:]).replace("'","") + str([row[0]])
        print(line)

def example_tt():
    # [eval | x1, ... , xn ]
    return [[0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1],
            [1, 0, 1, 1, 0]]


def example_tree():
  x1 = Node(1)
  x2 = Node(2, x1, False)
  x3 = Node(3, x1, True)
  x4 = Node(4, x2, False)
  x5 = Node(5, x3,  False)

  leafs = []
  leafs.append(Node(True, x4, False))
  leafs.append(Node(False, x4, True))
  leafs.append(Node(True, x2, True))
  leafs.append(Node(False, x3, True))
  leafs.append(Node(False, x5, False))
  leafs.append(Node(False, x5, True))
  return Tree(x1)

def tree_gen(nodes):
    def next(fst, lst, parent, path):
        new = Node(fst, parent, path)
        fst+=1
        if fst>lst:
            # leaves
            Node(True, new, True)
            Node(False, new, False)
            return
        else:
            split = int((fst+lst)/2)
            next(fst, split, new, True)
            next(split+1, lst, new, False)
        return new
        
    root = next(1, nodes, None, None)
    return Tree(root)


def complete_tree_valid(t):
    t.calculate_stats()
    return (2**t.depth-1) == t.nodes_amount

def algo_works(algo, tests=10, tt_size=5):
    valid = True
    for _ in range(tests):
        xs = randint(1, tt_size)
        tt = tt_gen(xs, randint(1, 2*xs))
        t = algo(tt)
        valid = valid and t.eval_table(tt)
    return valid

def verify(t, tt):
    if not t.eval_table(tt):
        raise Exception("tree not valid representation of truth table")
