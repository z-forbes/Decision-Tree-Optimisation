# Algorithms for Decision Tree Optimisation

This repo complements my UG4 project *Exploring Descriptive Decision Trees: Construction and Analysis*. It contains tree and node libraries, as well as a whole host of algorithms for decision tree construction and general data gathering for truth tables and decision trees.

For a very small number of truth tables, the optimal algorithm doesn't run. See [``failures.txt``](/failures.txt) for examples of such truth tables.

The file [``demo.py``](/demo.py) can be used to ensure everything is running as it should be, and highlights the capabilities of this repo.

The output of this file should be:

```
Here is a simple tree:
  _1_  
 /   \ 
 2   3 
/ \ / \
T F F T

The tree class has some helpful methods:
Root: x1
Depth: 3
Size: 7

Here is a simple truth table:
[1, 2, 3, 4] f
[0, 0, 1, 1][0]
[0, 0, 0, 1][1]
[0, 0, 0, 0][0]
[1, 1, 0, 1][1]
[1, 0, 1, 0][0]

Trees can be generated from truth tables using the algorithms in algos.py:
  _3 
 /  \
 4  F
/ \  
F T  
^tree created by the optimal algorithm

    _2 
   /  \
  _3  T
 /  \  
 4  F  
/ \    
F T    
^tree created by the c45 algorithm


algos.py has some useful functions beyond tree construction:
The truth table above can be represented by...
   -52 distinct trees.
   -2 distinct optimal trees.


failures.txt contains examples of truth tables for which the optimal algorithm raises an exception:

Finding optimal tree from the following truth table:
[1, 2, 3, 4, 5, 6] f
[0, 1, 1, 0, 0, 0][0]
[1, 0, 1, 0, 1, 0][0]
[1, 0, 1, 1, 0, 0][0]
[1, 1, 1, 1, 0, 1][0]
[0, 0, 1, 0, 0, 0][1]
[0, 0, 1, 1, 1, 0][1]
[0, 1, 0, 0, 0, 1][1]
[0, 1, 1, 1, 0, 0][1]
[1, 1, 1, 0, 0, 1][1]

There was an error!
```
