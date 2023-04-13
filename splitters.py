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