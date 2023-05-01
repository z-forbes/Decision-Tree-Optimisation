from algos import *
from utils import *
from random import randint, shuffle
from ast import literal_eval

def gen_failures():
    for i in range(1000):
        # print(i)
        xs = 6
        tt = tt_gen(xs, 11)
        try:
            optimal(tt)
        except:
            print("failure found: " + str(tt))
            f = open("failures.txt", "a")
            f.write(str(tt) + "\n")
            f.close

def parse_failures():
    output = []
    f = open("failures.txt", "r")
    for line in f:
        output.append(literal_eval(line))
    return output

# greedy algorithm
def shorten_failure(fail):
    if len(fail)==1:
        return fail
    
    for row in fail:
        new = fail[:]
        new.remove(row)
        still_fail=False
        try:
            optimal(new)
        except:
            return shorten_failure(new)
    return fail
         
# converts each tt in failures.txt to a shortened, sorted form   
def shorten_failures():
    output = ""
    tts = parse_failures()
    for tt in tts:
        tt = shorten_failure(tt)
        tt.sort()
        output += str(tt) + "\n"
    f = open("failures.txt", "w")
    f.write(output)
    f.close()

# gen_failures()
# shorten_failures()
# print("done")