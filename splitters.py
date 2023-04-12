from itertools import count
import math
from posixpath import split

###  INFORMATION GAIN (ID3) ###
def col_info_gain(tt, x_i, H_table=None):
    col = [row[x_i] for row in tt]
    evals = [row[0] for row in tt]
    col_evals = list(zip(col, evals))

    ig=0
    for a in [0,1]:
        H_current = entropy([ce[1] for ce in col_evals if ce[0]==a])
        p_current = col.count(a)/len(col)
        ig += H_current*p_current
    
    if H_table==None:
        H_table = entropy_of_table(tt)
    return H_table-ig

def entropy(X):
    X_size = len(X)
    Ts = X.count(1)
    Fs = X_size - Ts
    if Ts==0 or Fs==0:
        return 0
    
    H = 0
    for x in [Ts,  Fs]:
        p = x/X_size
        H += -(p * math.log(p, 2))
    return H

def entropy_of_table(tt):   
    return entropy([row[0] for row in tt])




### GINI IMPURITY (CART) ###
def col_gini_impurity(tt, x_i):
    col = [row[x_i] for row in tt]
    evals = [row[0] for row in tt]
    col_evals = list(zip(col, evals))
    
    output = 0 
    for a in [0,1]:
        # print(gini_imp([ce[1] for ce in col_evals if ce[0]==a]))
        output += p_a(col, a) * gini_imp([ce[1] for ce in col_evals if ce[0]==a])
    return output

def p_a(xs, a):
    return len([x for x in xs if x==a])/len(xs)

def gini_imp(xs):
    if not ((0 in xs) and (1 in xs)):
        return 0
    output = 1
    for a in [0,1]:
        output -= p_a(xs, a)**2
    return output

### INFORMATION GAIN RATIO (C4.5) ###
def col_gain_ratio(tt, x_i, ig=None):
    si = split_info([r[x_i] for r in tt])
    if si==0:
        return 0
    if ig==None:
        ig = col_info_gain(tt, x_i)
    return ig/si    
    
def split_info(X):
    sum = 0
    for a in [0,1]:
        c = X.count(a)
        if c==0:
            continue
        frac = c/len(X)
        sum += frac * math.log(frac, 2)
    return -sum




### TESTS ###
# https://medium.com/geekculture/step-by-step-decision-tree-id3-algorithm-from-scratch-in-python-no-fancy-library-4822bbfdd88f
# need to change [0,1] to [0,2,1] in ig_of_col().
def id3_test():
    # sunny=0, overcast=1, rain=2
    tt = [
        [0,0],
        [0,0],
        [1,1],
        [1,2],
        [1,2],
        [0,2],
        [1,1],
        [0,0],
        [1,0],
        [1,2],
        [1,0],
        [1,1],
        [1,1],
        [0,2]
    ]

    H_table = entropy_of_table(tt)
    print(H_table)
    print(col_info_gain(tt,1,H_table))


# https://medium.com/analytics-vidhya/classification-in-decision-tree-a-step-by-step-cart-classification-and-regression-tree-8e5f5228b11e
def cart_test():
    tt = []
    x1 = 0
    for _ in range(24):
        tt.append([0,x1])
    for _ in range(114):
        tt.append([1,x1])

    x1 = 1
    for _ in range(72):
        tt.append([0,x1])
    for _ in range(93):
        tt.append([1,x1])

    print(col_gini_impurity(tt, 1))


# https://en.wikipedia.org/wiki/Information_gain_ratio
def c45_test():
    # humidity | wind | play 
    tt = [[0, 1, 0], [0, 1, 1], [1, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 1], [1, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 0], [1, 0, 1], [1, 1, 1], [1, 0, 0], [0, 1, 1]]
    tt = [[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1],[0,1],[1,1]]
    print(split_info([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))

