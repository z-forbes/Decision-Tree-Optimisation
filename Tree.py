class Tree:

  def __str__(self):
    def old():
      if self.root.is_leaf():
          return str(self.root)
      
      self.mk_nodes()
      most_left = 0
      for depth in self.nodes:
        for n in depth:
          if n[1] < most_left:
            most_left = n[1]
      output = ""
      for depth in self.nodes:
        line = ""
        for n in depth:
          relative_pos = n[1]-most_left
          #   line += " "*(relative_pos-len(line))
          line += "  "*round(0.1+relative_pos-(len(line)/2))
          line += str(n[0])[1]
        output += line + "\n"
    
      return output
    return self.root.tree_to_string()
    
  # subtrees = [left_st, right_st]
  def __init__(self, root, subtrees=[]):
    self.root = root
    self.depth = 0
    self.nodes_amount = 0 
    self.leaves_amount = 0

    # construst tree if subtrees given
    if len(subtrees)==0:
      pass
    elif len(subtrees)!=2 or len(root.children) != 0:
      raise Exception("len(subtrees)={}, root.children={}".format(len(subtrees), root.children))
    else:
      for st in subtrees:
        st.root.set_parent(self.root)
        st.mk_nodes()
        st.root.depth -= 1 # to account for double increment
        for d in st.nodes:
          for n in d:
            n[0].depth += 1

    
    self.calculate_stats() # does not calculate self.nodes
    self.nodes = [[]] # [[(Node, indent)]] # mk_nodes() to generate
    
  # CHECKS IF TREE SATISFIES GIVEN VARIABLE ASSIGNMENT
  # assignment indexed from 0
  def eval(self, assignments):
    if self.root == None:
      return None
    
    current_node = self.root
    while not current_node.is_leaf():
      assignment = assignments[current_node.value-1]
      if assignment == False:
        current_node = current_node.children[0]
      elif assignment == True:
        current_node = current_node.children[1]
      else:
        raise Exception("Invalid assignment: {}".format(assignment))

    return current_node.value

  # TAKES A LIST OF BOOLEANS, WORKS DOWN ONE PATH. 
  # RETURNS WHERE ENDS UP
  def chain_eval(self, bool_arr):
    if self.root == None:
      return None
    
    current = self.root
    for b in bool_arr:
      if current.is_leaf():
        return None # too many bools provided

      children = current.children
      if len(children)!=2:
        raise Exception("Node {} has {} child(ren)".format(current, len(children)))
      
      if not b:
        current = children[0]
      else:
        current = children[1]
    
    return current #node or leaf
  
  # CHECKS IF TREE SATISFIES TABLE
  def eval_table(self, table, show_errors=True):
    passed = True
    for row in table:
      if self.eval(row[1:]) != row[0]: # 0=False, 1=True so mixed comparison okay
        passed = False
        if show_errors:
          print("Tree does not satisfy {}{}.".format(row[1:], [row[0]]))
    return passed

  # calculates __init__ attributes
  def calculate_stats(self):
    if self.root.is_leaf():
        self.depth = 1
        self.nodes = [[self.root]]
        self.nodes_amount = 1
        return

    # appends false to an eval list until it reaches a leaf 
    def reach_leafs(arr):
      while not(self.chain_eval(arr).is_leaf()):
        arr.append(False)
  
    # generates the next path
    def inc(arr):
      if arr[len(arr)-1] == False:
        arr[len(arr)-1] = True
        reach_leafs(arr) # arr.append([False,...,False])
        return arr
      else:
        arr = arr[0:len(arr)-1]
        return inc(arr)

    current_eval = [False]
    reach_leafs(current_eval) # [False,...,False]
    max_depth = self.chain_eval(current_eval).depth
    paths = 1
    while False in current_eval: # all true means all possibilities tried
      current_eval = inc(current_eval)
      paths+=1
      current_depth = self.chain_eval(current_eval).depth

      if current_depth > max_depth: 
        max_depth = current_depth

    self.depth = max_depth
    self.leaves_amount = paths
    self.nodes_amount = (2*paths)-1 # https://bit.ly/3UcZHkK


  # GENERATES SELF.NODES
  # second tuple value is useless - should remove
  def mk_nodes(self):
    if (self.root.is_leaf()):
      self.nodes = [[(self.root, 0)]]
      return
    
    def add_node(current_arr):
      current_node = self.chain_eval(current_arr)
      trues = sum(current_arr)
      falses = len(current_arr) - trues
      self.nodes[current_node.depth-1].append((current_node, trues-falses))
      

    def reach_leafs(arr):
      while not(self.chain_eval(arr).is_leaf()):
        arr.append(False)
        add_node(arr)
  
    def inc(arr):
      if arr[len(arr)-1] == False:
        arr[len(arr)-1] = True
        add_node(arr)
        reach_leafs(arr) # arr.append([False,...,False])
        return arr
      else:
        arr = arr[0:len(arr)-1]
        return inc(arr)

    if self.root == None:
      self.nodes = [[]]
      return 
    
    if self.root.is_leaf():
      self.nodes = [[self.root]]
      return
    
    self.calculate_stats()
    self.nodes = [[] for temp in range(self.depth)]
    self.nodes[0].append((self.root,0))
    current_eval = [False]
    add_node(current_eval)

    reach_leafs(current_eval) # [False,...,False]
    while False in current_eval:
      current_eval = inc(current_eval)