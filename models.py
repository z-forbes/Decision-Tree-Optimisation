import math
from random import randint, random
from algos import *
from utils import tt_gen

def model1(xs,rs):
    a=1.01
    b=0.7
    return a*rs*((math.exp(b)/2)**xs)

def model2(xs,rs):
    m = 1.042
    c = 0.0495
    b = 0.72
    return math.exp(b*xs)*(m*(rs/2**xs)-c)

def pct_dif(truth, value):
    return abs(value-truth)/truth


algo = optimal
tests = 10000
count = 0


print(algo.__name__)
for t in range(tests):
    print(t)
    if t%500==0:
        print(t)
    xs = randint(5,15)
    rs = randint(1, round(0.3333*2**xs))
    truth = algo(tt_gen(xs, rs)).nodes_amount
    count+= pct_dif(truth,model1(xs, rs))
count = count/tests
print(count)

print("end")
f = open("output.txt" , "w")
f.write(str(count))
f.close()
