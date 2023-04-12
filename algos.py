from Tree import *
from Node import *
from splitters import col_gain_ratio, col_gini_impurity, col_info_gain
from utils import *


# # splits on x1 then x2 then ... then xn
def topdown(truth_table):
    # returns the root node #
    # bag:          rows of truth tables to be classified still (values)
    # remaining:    attributes not on path above (indexes from 1)
    # parent_node:  [Node]
    # parent_path:  truth of path leading to attriubte
    def split(bag, remaining, parent_node, parent_path):
        if len(bag)==0:
            Node(True, parent_node, parent_path) # value is arbitrary
            return 

        if len(set([row[0] for row in bag]))==1: # all rows in bag have the same eval
            Node(bool(bag[0][0]), parent_node, parent_path)
            return

        split_on = remaining[0]
        new_node = Node(split_on, parent_node, parent_path)

        left_bag = [row for row in bag if row[split_on]==0]
        right_bag = [row for row in bag if row[split_on]==1]

        new_remaining = remaining.copy()
        new_remaining.remove(split_on)
        split(left_bag, new_remaining, new_node, False)
        split(right_bag, new_remaining, new_node, True)

        if parent_path==None:
            return new_node

    evals = [row[0] for row in truth_table]
    if len(set(evals))==1:
        return Tree(Node(bool(evals[0])))
    else:
        return Tree(split(truth_table, [i for i in range(1, len(truth_table[0]))], None, None))


# splits on attribute with highest information gain
def id3(truth_table):
    def choose_split(remaining, bag):
        if len(remaining)==0:
            raise Exception("remaining empty")
        max_ig = -1 # lowest possible ig is 0
        choice = 0 # no x_0
        for x_i in remaining:
            current_ig = col_info_gain(bag, x_i)
            if current_ig > max_ig:
                max_ig = current_ig
                choice = x_i
        return choice

    # returns the root node #
    # bag:          rows of truth tables to be classified still (values)
    # remaining:    attributes not on path above (indexes from 1)
    # parent_node:  [Node]
    # parent_path:  truth of path leading to attriubte
    def split(bag, remaining, parent_node, parent_path):
        if len(bag)==0:
            Node(True, parent_node, parent_path) # value is arbitrary
            return 

        if len(set([row[0] for row in bag]))==1: # all rows in bag have the same eval
            Node(bool(bag[0][0]), parent_node, parent_path)
            return

        split_on = choose_split(remaining, bag)
        new_node = Node(split_on, parent_node, parent_path)

        left_bag = [row for row in bag if row[split_on]==0]
        right_bag = [row for row in bag if row[split_on]==1]

        new_remaining = remaining.copy()
        new_remaining.remove(split_on)
        split(left_bag, new_remaining, new_node, False)
        split(right_bag, new_remaining, new_node, True)

        if parent_path==None:
            return new_node

    evals = [row[0] for row in truth_table]
    if len(set(evals))==1:
        return Tree(Node(bool(evals[0])))
    else:
        return Tree(split(truth_table, [i for i in range(1, len(truth_table[0]))], None, None))


def double_id3(truth_table):
    # returns the sum of the max informtion gain of the possible roots of the subtrees
    def deep_max_ig(p_bag, p_remaining, x_i):
        c_remaining = [x for x in p_remaining if x!=x_i]
        c_bags = [[r for r in p_bag if r[x_i]==0],[r for r in p_bag if r[x_i]==1]]
        if len(c_bags[0])==0 or len(c_bags[1])==0:
            return 0
        
        sum = 0
        if len(set([r[0] for r in c_bags[0]]))==1:
            sum+=2
            if len(set([r[0] for r in c_bags[1]]))==1:
                sum+=2
            return sum
    
        for bag in c_bags:
            max_ig = -1 # lowest possible ig is 0
            for x_i in c_remaining:
                current_ig = col_info_gain(bag, x_i)
                if current_ig > max_ig:
                    max_ig = current_ig
            sum += max_ig 
        return sum


    def choose_split(remaining, bag):
        if len(remaining)==0:
            raise Exception("remaining empty")
        max_dig = -1 # lowest possible ig is 0
        choice = 0 # no x_0
        for x_i in remaining:
            current_ig = col_info_gain(bag, x_i)
            if current_ig==1:
                return x_i
            current_dig = deep_max_ig(bag, remaining, x_i)+current_ig
            if current_dig > max_dig:
                max_dig = current_dig
                choice = x_i
        return choice

    # returns the root node #
    # bag:          rows of truth tables to be classified still (values)
    # remaining:    attributes not on path above (indexes from 1)
    # parent_node:  [Node]
    # parent_path:  truth of path leading to attriubte
    def split(bag, remaining, parent_node, parent_path):
        if len(bag)==0:
            Node(True, parent_node, parent_path) # value is arbitrary
            return 

        if len(set([row[0] for row in bag]))==1: # all rows in bag have the same eval
            Node(bool(bag[0][0]), parent_node, parent_path)
            return

        split_on = choose_split(remaining, bag)
        new_node = Node(split_on, parent_node, parent_path)

        left_bag = [row for row in bag if row[split_on]==0]
        right_bag = [row for row in bag if row[split_on]==1]

        new_remaining = remaining.copy()
        new_remaining.remove(split_on)
        split(left_bag, new_remaining, new_node, False)
        split(right_bag, new_remaining, new_node, True)

        if parent_path==None:
            return new_node

    evals = [row[0] for row in truth_table]
    if len(set(evals))==1:
        return Tree(Node(bool(evals[0])))
    else:
        return Tree(split(truth_table, [i for i in range(1, len(truth_table[0]))], None, None))



# splits on attribute with the lowest gini impurity
def cart(truth_table):
    def choose_split(remaining, bag):
        if len(remaining)==0:
            raise Exception("remaining empty")
        min_gi = 1.1 # highest possible gi is 1
        choice = 0 # no x_0
        for x_i in remaining:
            current_gi = col_gini_impurity(bag, x_i)
            if current_gi < min_gi:
                min_gi = current_gi
                choice = x_i
        return choice

    # returns the root node #
    # bag:          rows of truth tables to be classified still (values)
    # remaining:    attributes not on path above (indexes from 1)
    # parent_node:  [Node]
    # parent_path:  truth of path leading to attriubte
    def split(bag, remaining, parent_node, parent_path):
        if len(bag)==0:
            Node(True, parent_node, parent_path) # value is arbitrary
            return 

        if len(set([row[0] for row in bag]))==1: # all rows in bag have the same eval
            Node(bool(bag[0][0]), parent_node, parent_path)
            return

        split_on = choose_split(remaining, bag)
        new_node = Node(split_on, parent_node, parent_path)

        left_bag = [row for row in bag if row[split_on]==0]
        right_bag = [row for row in bag if row[split_on]==1]

        new_remaining = remaining.copy()
        new_remaining.remove(split_on)
        split(left_bag, new_remaining, new_node, False)
        split(right_bag, new_remaining, new_node, True)

        if parent_path==None:
            return new_node

    evals = [row[0] for row in truth_table]
    if len(set(evals))==1:
        return Tree(Node(bool(evals[0])))
    else:
        return Tree(split(truth_table, [i for i in range(1, len(truth_table[0]))], None, None))


def c45(truth_table):
    def choose_split(remaining, bag):
        if len(remaining)==0:
            raise Exception("remaining empty")
        max_igr = -1 # lowest possible igr is 0
        choice = 0 # no x_0
        for x_i in remaining:
            current_igr = col_gain_ratio(bag, x_i)
            if current_igr > max_igr:
                max_igr = current_igr
                choice = x_i
        return choice

    # returns the root node #
    # bag:          rows of truth tables to be classified still (values)
    # remaining:    attributes not on path above (indexes from 1)
    # parent_node:  [Node]
    # parent_path:  truth of path leading to attriubte
    def split(bag, remaining, parent_node, parent_path):
        if len(bag)==0:
            Node(True, parent_node, parent_path) # value is arbitrary
            return 

        if len(set([row[0] for row in bag]))==1: # all rows in bag have the same eval
            Node(bool(bag[0][0]), parent_node, parent_path)
            return

        split_on = choose_split(remaining, bag)
        new_node = Node(split_on, parent_node, parent_path)

        left_bag = [row for row in bag if row[split_on]==0]
        right_bag = [row for row in bag if row[split_on]==1]

        new_remaining = remaining.copy()
        new_remaining.remove(split_on)
        split(left_bag, new_remaining, new_node, False)
        split(right_bag, new_remaining, new_node, True)

        if parent_path==None:
            return new_node

    evals = [row[0] for row in truth_table]
    if len(set(evals))==1:
        return Tree(Node(bool(evals[0])))
    else:
        return Tree(split(truth_table, [i for i in range(1, len(truth_table[0]))], None, None))


# condiders all options to find the optimal tree
def optimal(truth_table):
    # tt_valid(truth_table)

    # CONVERTS A LIST OF INDEXES TO A BINARY NUMBER
    # if i is in the list, binary number has 1 in ith position (indexed from 0), 0 otherwise
    # [1,3,4] -> 01011 -> 11
    def get_memo_index(attr_arr,length):
        if len(attr_arr)==0:
            return 0
        
        # converts the attribute array to a binary int()
        output = [0 for _ in range(length)]
        for i in attr_arr:
            output[i] = 1
            # output[length-1] = 1 # for reverse indexing
        binary_i = "".join(map(str, output))
        
        # converts the binary int into a decimal int
        dec_i = 0
        temp = binary_i[::-1]
        for i in range(len(temp)):
            if temp[i] == "0":
                continue
            if temp[i] == "1":
                dec_i += 2**i
            else:
                raise Exception("i: {}, temp[i]: {}".format(i,temp[i]))

        return dec_i
    
    def memoize_and_return(tree, xs, rs, total_xs_len, total_rs_len): ### store root not tree?
        constructed[get_memo_index(rs, total_rs_len)][get_memo_index(xs, total_xs_len)] = tree
        return tree
    
    # MAKES NEW rs BASED ON AN ATTRIBUTE ASSIGNMENT
    def new_rs(rs, x, truth):
        new = []
        for r in rs:
            if truth_table[r][x] == truth: # 0==False, 1==True -> True, True
                new.append(r)
        return new


    # RETURNS THE SMALLEST TREE THAT SATISFIES PARTIAL TT REFS GIVEN WITH UNUSED XS GIVEN 
    # xs    unassigned attributes
    # rs    indexes (from 0) of rows of truth table to be classified
    def min_tree(xs, rs, total_xs_len, total_rs_len):
        # CHECKS IF ALL REMAINING ROWS HAVE SAME EVAL. RETURN EITHER False OR Tree(Leaf())
        def finished(rs):
            to_match = truth_table[rs[0]][0]
            for i in rs:
                if truth_table[i][0] != to_match:
                    return False
            return Tree(Node(bool(to_match)))
        
        # check if already computed, if so return memoised tree
        memo_xs_i = get_memo_index(xs, total_xs_len)
        memo_rs_i = get_memo_index(rs, total_rs_len)
        if constructed[memo_rs_i][memo_xs_i] != None:
            return constructed[memo_rs_i][memo_xs_i]

        if len(rs)==0:
            # input("empty bag")
            return Tree(Node(False))

        temp = finished(rs)
        if temp != False:
            return memoize_and_return(temp, xs, rs, total_xs_len, total_rs_len)

        output = None
        os_default = -1
        output_size = os_default
        if len(xs) != 0:
            for x in xs:
                # if no gain from splitting, skip
                left_rs = new_rs(rs, x, False)
                right_rs = new_rs(rs, x, True)
                x_useless = False
                for r in [left_rs, right_rs]:
                    if len(r)==len(rs):
                        temp = finished(r)
                        if temp==False:
                            x_useless = True
                            break
                        else: # else never reached i think????
                            raise Exception("else reached")
                if x_useless:
                    continue

                unused_xs = xs.copy()
                unused_xs.remove(x)
                left = min_tree(unused_xs, left_rs, total_xs_len, total_rs_len) 
                right = min_tree(unused_xs, right_rs, total_xs_len, total_rs_len)
                current = Tree(Node(x), [left, right])
                current_size = current.nodes_amount
                if (current_size < output_size) or (output_size == os_default):
                    output = current
                    output_size = current_size
            return memoize_and_return(output, xs, rs, total_xs_len, total_rs_len)
        else:
            temp = finished(rs)
            if temp == False:
                raise Exception("xs = {}, rs = {}".format(xs, rs))
            else:
                return memoize_and_return(temp, xs, rs, total_xs_len, total_rs_len)
    ##### end of min_tree() #####
    
    # constructed[a][b], a=0 or b=0 will remain None - list indexes from 1
    constructed = [None for _ in range(2**(len(truth_table[0])-1))] # variables to be assigned
    constructed = [constructed.copy() for _ in range(2**len(truth_table))] # truth table rows still to be considered            

    xs = [(x+1) for x in range(len(truth_table[0])-1)]  # [1,...]
    rs = [r for r in range(len(truth_table))]         # [0,...]
    return min_tree(xs, rs, len(xs)+1, len(rs))


# counts all plausable trees for a given table
def count_trees(truth_table):
    # tt_valid(truth_table)

    # CONVERTS A LIST OF INDEXES TO A BINARY NUMBER
    # if i is in the list, binary number has 1 in ith position (indexed from 0), 0 otherwise
    # [1,3,4] -> 01011 -> 11
    def get_memo_index(attr_arr,length):
        if len(attr_arr)==0:
            return 0
        
        # converts the attribute array to a binary int()
        output = [0 for _ in range(length)]
        for i in attr_arr:
            output[i] = 1
            # output[length-1] = 1 # for reverse indexing
        binary_i = "".join(map(str, output))
        
        # converts the binary int into a decimal int
        dec_i = 0
        temp = binary_i[::-1]
        for i in range(len(temp)):
            if temp[i] == "0":
                continue
            if temp[i] == "1":
                dec_i += 2**i
            else:
                raise Exception("i: {}, temp[i]: {}".format(i,temp[i]))

        return dec_i
    
    def memoize_and_return(count, xs, rs, total_xs_len, total_rs_len): 
        constructed[get_memo_index(rs, total_rs_len)][get_memo_index(xs, total_xs_len)] = count
        return count 
    
    # MAKES NEW rs BASED ON AN ATTRIBUTE ASSIGNMENT
    def new_rs(rs, x, truth):
        new = []
        for r in rs:
            if truth_table[r][x] == truth: # 0==False, 1==True -> True, True
                new.append(r)
        return new


    # RETURNS THE SMALLEST TREE THAT SATISFIES PARTIAL TT REFS GIVEN WITH UNUSED XS GIVEN 
    # xs    unassigned attributes
    # rs    indexes (from 0) of rows of truth table to be classified
    def subcount(xs, rs, total_xs_len, total_rs_len):
        # true <=> all rows have the same eval
        def finished(rs):
            to_match = truth_table[rs[0]][0]
            for i in rs:
                if truth_table[i][0] != to_match:
                    return False
            return True
        
        # check if already computed, if so return memoised count
        memo_xs_i = get_memo_index(xs, total_xs_len)
        memo_rs_i = get_memo_index(rs, total_rs_len)
        if constructed[memo_rs_i][memo_xs_i] != None:
            return constructed[memo_rs_i][memo_xs_i]

        # no more rows to classify
        if len(rs)==0:
            return 2 # true or false

        if finished(rs):
            return memoize_and_return(1, xs, rs, total_xs_len, total_rs_len) # only one tree possible

        if len(xs) != 0:
            current = 0
            for x in xs:
                left_rs = new_rs(rs, x, False)
                right_rs = new_rs(rs, x, True)
                unused_xs = xs.copy()
                unused_xs.remove(x)
                left_count = subcount(unused_xs, left_rs, total_xs_len, total_rs_len) 
                right_count = subcount(unused_xs, right_rs, total_xs_len, total_rs_len)
                current += (left_count * right_count) # rs disjoint
                
            return memoize_and_return(current, xs, rs, total_xs_len, total_rs_len)
        else:
            if not finished(rs):
                raise Exception("xs = {}, rs = {}".format(xs, rs))
            else:
                return memoize_and_return(1, xs, rs, total_xs_len, total_rs_len)
    ##### end of min_tree() #####
    
    # constructed[a][b], a=0 or b=0 will remain None - list indexes from 1
    constructed = [None for _ in range(2**(len(truth_table[0])-1))] # variables to be assigned
    constructed = [constructed.copy() for _ in range(2**len(truth_table))] # truth table rows still to be considered            

    xs = [(x+1) for x in range(len(truth_table[0])-1)]  # [1,...]
    rs = [r for r in range(len(truth_table))]         # [0,...]
    return subcount(xs, rs, len(xs)+1, len(rs))


# generates all optimal trees for a given table
def gen_optimal(truth_table):
    # tt_valid(truth_table)

    # CONVERTS A LIST OF INDEXES TO A BINARY NUMBER
    # if i is in the list, binary number has 1 in ith position (indexed from 0), 0 otherwise
    # [1,3,4] -> 01011 -> 11
    def get_memo_index(attr_arr,length):
        if len(attr_arr)==0:
            return 0
        
        # converts the attribute array to a binary int()
        output = [0 for _ in range(length)]
        for i in attr_arr:
            output[i] = 1
            # output[length-1] = 1 # for reverse indexing
        binary_i = "".join(map(str, output))
        
        # converts the binary int into a decimal int
        dec_i = 0
        temp = binary_i[::-1]
        for i in range(len(temp)):
            if temp[i] == "0":
                continue
            if temp[i] == "1":
                dec_i += 2**i
            else:
                raise Exception("i: {}, temp[i]: {}".format(i,temp[i]))

        return dec_i
    
    def memoize_and_return(trees, xs, rs, total_xs_len, total_rs_len): ### store root not tree?
        constructed[get_memo_index(rs, total_rs_len)][get_memo_index(xs, total_xs_len)] = trees
        return trees
    
    # MAKES NEW rs BASED ON AN ATTRIBUTE ASSIGNMENT
    def new_rs(rs, x, truth):
        new = []
        for r in rs:
            if truth_table[r][x] == truth: # 0==False, 1==True -> True, True
                new.append(r)
        return new


    # RETURNS ALL OPTIMAL TREES THAT SATISFIES PARTIAL TT REFS GIVEN WITH UNUSED XS GIVEN 
    # xs    unassigned attributes
    # rs    indexes (from 0) of rows of truth table to be classified
    def subgen(xs, rs, total_xs_len, total_rs_len):
        # CHECKS IF ALL REMAINING ROWS HAVE SAME EVAL. RETURN EITHER False OR Tree(Leaf())
        def finished(rs):
            to_match = truth_table[rs[0]][0]
            for i in rs:
                if truth_table[i][0] != to_match:
                    return False
            return [Tree(Node(bool(to_match)))]
        
        # check if already computed, if so return memoised tree
        memo_xs_i = get_memo_index(xs, total_xs_len)
        memo_rs_i = get_memo_index(rs, total_rs_len)
        if constructed[memo_rs_i][memo_xs_i] != None:
            return constructed[memo_rs_i][memo_xs_i]

        if len(rs)==0:
            return [Tree(Node(False)), Tree(Node(True))]

        temp = finished(rs)
        if temp != False:
            return memoize_and_return(temp, xs, rs, total_xs_len, total_rs_len)

        output = []
        if len(xs) != 0:
            opt_size = optimal([truth_table[r] for r in rs]).nodes_amount
            for x in xs:
                # if no gain from splitting, skip
                left_rs = new_rs(rs, x, False)
                right_rs = new_rs(rs, x, True)

                unused_xs = xs.copy()
                unused_xs.remove(x)
                lefts = subgen(unused_xs, left_rs, total_xs_len, total_rs_len) 
                rights = subgen(unused_xs, right_rs, total_xs_len, total_rs_len)
                for l in lefts:
                    for r in rights:
                        current = Tree(Node(x), [l,r])
                        if current.nodes_amount==opt_size:
                            output.append(current)
                
            return memoize_and_return(output, xs, rs, total_xs_len, total_rs_len)
        else:
            temp = finished(rs)
            if temp == False:
                raise Exception("xs = {}, rs = {}".format(xs, rs))
            else:
                return memoize_and_return(temp, xs, rs, total_xs_len, total_rs_len)
    ##### end of min_tree() #####
    
    # constructed[a][b], a=0 or b=0 will remain None - list indexes from 1
    constructed = [None for _ in range(2**(len(truth_table[0])-1))] # variables to be assigned
    constructed = [constructed.copy() for _ in range(2**len(truth_table))] # truth table rows still to be considered            

    xs = [(x+1) for x in range(len(truth_table[0])-1)]  # [1,...]
    rs = [r for r in range(len(truth_table))]         # [0,...]
    return subgen(xs, rs, len(xs)+1, len(rs))

# tt = [[0, 1, 1, 0, 0, 1], [0, 1, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0], [1, 1, 0, 0, 1, 1], [0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 1, 0], [0, 1, 1, 1, 0, 1], [0, 0, 0, 0, 1, 1], [1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 1, 1], [1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1], [1, 0, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1]]
# generates all plausable trees for a given table
def gen_trees(truth_table):
    # tt_valid(truth_table)

    # CONVERTS A LIST OF INDEXES TO A BINARY NUMBER
    # if i is in the list, binary number has 1 in ith position (indexed from 0), 0 otherwise
    # [1,3,4] -> 01011 -> 11
    def get_memo_index(attr_arr,length):
        if len(attr_arr)==0:
            return 0
        
        # converts the attribute array to a binary int()
        output = [0 for _ in range(length)]
        for i in attr_arr:
            output[i] = 1
            # output[length-1] = 1 # for reverse indexing
        binary_i = "".join(map(str, output))
        
        # converts the binary int into a decimal int
        dec_i = 0
        temp = binary_i[::-1]
        for i in range(len(temp)):
            if temp[i] == "0":
                continue
            if temp[i] == "1":
                dec_i += 2**i
            else:
                raise Exception("i: {}, temp[i]: {}".format(i,temp[i]))

        return dec_i
    
    def memoize_and_return(trees, xs, rs, total_xs_len, total_rs_len): ### store root not tree?
        constructed[get_memo_index(rs, total_rs_len)][get_memo_index(xs, total_xs_len)] = trees
        return trees
    
    # MAKES NEW rs BASED ON AN ATTRIBUTE ASSIGNMENT
    def new_rs(rs, x, truth):
        new = []
        for r in rs:
            if truth_table[r][x] == truth: # 0==False, 1==True -> True, True
                new.append(r)
        return new


    # RETURNS ALL TREES THAT SATISFIES PARTIAL TT REFS GIVEN WITH UNUSED XS GIVEN 
    # xs    unassigned attributes
    # rs    indexes (from 0) of rows of truth table to be classified
    def subgen(xs, rs, total_xs_len, total_rs_len):
        # CHECKS IF ALL REMAINING ROWS HAVE SAME EVAL. RETURN EITHER False OR Tree(Leaf())
        def finished(rs):
            to_match = truth_table[rs[0]][0]
            for i in rs:
                if truth_table[i][0] != to_match:
                    return False
            return [Tree(Node(bool(to_match)))]
        
        # check if already computed, if so return memoised tree
        memo_xs_i = get_memo_index(xs, total_xs_len)
        memo_rs_i = get_memo_index(rs, total_rs_len)
        if constructed[memo_rs_i][memo_xs_i] != None:
            return constructed[memo_rs_i][memo_xs_i]

        if len(rs)==0:
            return [Tree(Node(False)), Tree(Node(True))]

        temp = finished(rs)
        if temp != False:
            return memoize_and_return(temp, xs, rs, total_xs_len, total_rs_len)

        output = []
        if len(xs) != 0:
            for x in xs:
                # if no gain from splitting, skip
                left_rs = new_rs(rs, x, False)
                right_rs = new_rs(rs, x, True)

                unused_xs = xs.copy()
                unused_xs.remove(x)
                lefts = subgen(unused_xs, left_rs, total_xs_len, total_rs_len) 
                rights = subgen(unused_xs, right_rs, total_xs_len, total_rs_len)
                for l in lefts:
                    for r in rights:
                        output.append(Tree(Node(x), [l,r]))
            return memoize_and_return(output, xs, rs, total_xs_len, total_rs_len)
        else:
            temp = finished(rs)
            if temp == False:
                raise Exception("xs = {}, rs = {}".format(xs, rs))
            else:
                return memoize_and_return(temp, xs, rs, total_xs_len, total_rs_len)
    ##### end of min_tree() #####
    
    # constructed[a][b], a=0 or b=0 will remain None - list indexes from 1
    constructed = [None for _ in range(2**(len(truth_table[0])-1))] # variables to be assigned
    constructed = [constructed.copy() for _ in range(2**len(truth_table))] # truth table rows still to be considered            

    xs = [(x+1) for x in range(len(truth_table[0])-1)]  # [1,...]
    rs = [r for r in range(len(truth_table))]         # [0,...]
    return subgen(xs, rs, len(xs)+1, len(rs))

