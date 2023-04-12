from algos import *
from utils import *
import numpy as np
import matplotlib.pyplot as plt
import splitters
from time import process_time
import math
import matplotlib as mpl

### CHAPTER 1: INTRODUCTION ###
def comparison_tt(do_output=True):
    def f_old(a,b,c,d):
        output = ((not a) and c and d)
        output = output or ((not a) and (not c) and (not d))
        output = output or ((not b) and d)
        return int(output)
    
    def f(a,b,c):
        output = (a and (not b) and c)
        output = output or ((not a) and b)
        output = output or (b and (not c))
        return int(output)
    
    tt = []
    current = 0b0
    while current <= 0b111:
        cur_str = bin(current)[2:]
        cur_str = "0"*(3-len(cur_str)) + cur_str
        row = [cur_str[0], cur_str[1], cur_str[2]]
        row = [int(x) for x in row]
        row = [f(row[0], row[1], row[2])] + row
        tt.append(row)
        current += 0b1
    
    if do_output:
        f = open(save_dir()+"output.tex", 'w')
        f.write(tt_to_latex(tt))
        f.close()
    else:
        return tt
        
def comparison_tree(do_output=True):
    t = optimal(comparison_tt(False))
    if do_output:
        f = open(save_dir()+"output.tex", 'w')
        f.write(tree_to_latex(t))
        f.close()
    else:
        return t



### CHAPTER 2: BACKGROUND ###
## helper functions ##
def tt_to_latex(tt):
    output = "\\begin{displaymath}\n\\begin{array}"
    output += "{" + "|{}|c|".format("c "*(len(tt[0])-1)) + "}\n"
    for x_i in range(1,len(tt[0])):
        output += "x_{} & ".format(x_i)
    output += "\\textrm{f}\\\\\n\\hline\n"
    for row in tt:
        temp = ""
        for e in row[1:]:
            temp += str(e) + " & "
        temp += str(row[0])
        
        output += temp + " \\\\\n"
    output += "\\end{array}\n\\end{displaymath}"
    # source = "% https://people.engr.tamu.edu/hlee42/csce222/truth-table.pdf"
    return output

def tree_to_latex(tree):
    def node_label(node):
        if node.is_leaf():
            return str(int(node.value))
        else:
            return "$x_{}$".format(node.value)

    def subtree(rt, path):
        if rt.is_leaf():
            return node_label(rt)
        dashed = ""
        if not path:
            dashed = ", edge=dashed"
        return "{} {} [{}, edge=dashed] [{}]".format(node_label(rt), dashed, subtree(rt.children[0], False), subtree(rt.children[1], True))

    root = tree.root
    output = "[{} [{}, edge=dashed] [{}]]".format(node_label(root), subtree(root.children[0], False), subtree(root.children[1], True))
    # source = "% https://tex.stackexchange.com/questions/289642/how-to-draw-a-proper-decision-tree"
    return "\\begin{forest}\n\t" + output + "\n\\end{forest}"

def output(string):
    f = open(save_dir() + "output.tex", "w")
    f.write(string)
    f.close()
## figures ##
def truth_table(do_output=True):
    tt = [[0, 0, 1, 0, 1, 0], [0, 1, 1, 1, 0, 1], [0, 0, 1, 0, 0, 0], [1, 1, 1, 0, 0, 1], [1, 0, 1, 0, 1, 1], [1, 0, 0, 1, 1, 1], [1, 0, 1, 1, 0, 0], [0, 1, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1], [1, 1, 0, 1, 1, 0], [1, 0, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 0]]
    tt = tt[1:-6]
    if do_output:
        output(tt_to_latex(tt))
    return tt

def big_tree(do_output=True):
    tree = topdown(truth_table(False))
    if do_output:
        output(tree_to_latex(tree))
    return tree

def medium_tree(do_output=True):
    tree = id3(truth_table(False))
    if do_output:
        output(tree_to_latex(tree))
    return tree


def small_tree(do_output=True):
    tree = optimal(truth_table(False))
    if do_output:
        output(tree_to_latex(tree))
    return tree


### CHAPTER 3: ALGORITHMS ###
def uc_tt(do_output=True):
    tt = [[1, 1, 1, 1, 0, 1], [1, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 0], [1, 0, 0, 1, 1, 1], [0, 0, 1, 0, 0, 1]]
    
    if do_output:
        output(tt_to_latex(tt))
    else:
        return tt

def uc_tree(do_output=True):
    t = optimal(uc_tt(False))
    if do_output:
        output(tree_to_latex(t))
    else:
        print(t)


### CHAPTER 4: EXPERIMENTS ###
## helper functions ##
def precision():
    return "precision"

def save_dir():
    return "figures/"

## figures
def rel_row_increase(save=True):
    def get_data(xs, tests):
        print(xs)

        total = 2**xs
        ks = [(x/10) for x in range(1, 11)]

        output=[]
        for k in ks:
            current = 0
            for t in range(tests):
                current += id3(tt_gen(xs, int(k*total))).nodes_amount
            output.append((k, current/tests))
        return output

    tests = 1000
    plt.title("[{}: {}]".format(precision(), tests))
    plt.xlabel("Value of α")
    plt.ylabel("Tree size (nodes)")

    for xs in [4,6,8,10,12]:
        data = get_data(xs, tests)
        plt.plot([x[0] for x in data], [x[1] for x in data], label="xs={}".format(xs))

    plt.legend()
    if save:
        fname = "rel_row_increase.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def abs_row_increase(save=True):
    def get_data(xs, tests, min_rs=2, max_rs=10):
        print(xs)
        output=[]
        for rs in range(min_rs, max_rs+1):
            current = 0
            for t in range(tests):
                current += id3(tt_gen(xs, rs)).nodes_amount
            output.append((rs, current/tests))
        return output

    tests = 1000
    plt.title("[{}: {}]".format(precision(), tests))
    plt.xlabel("Rows in truth table")
    plt.ylabel("Tree size (nodes)")

    for xs in [5,6,8,10,15,30]:
        data = get_data(xs, tests)
        plt.plot([x[0] for x in data], [x[1] for x in data], label="xs={}".format(xs))

    plt.legend()
    
    if save:
        fname = "abs_row_increase.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()

def h_performance_line(save=True):
    def get_data(min_xs, max_xs, tests, heuristic):
        output=[]
        for xs in range(min_xs, max_xs+1):
            print(xs)
            current = 0
            for _ in range(tests):
                tt = tt_gen(xs, int((2**xs)/2))
                current += heuristic(tt).nodes_amount
            output.append((xs, current/tests))
        return output

    tests = 1000
    plt.xlabel("Number of attributes")
    plt.ylabel("Tree size (nodes)")
    plt.title("[rs=(2^xs)/2, {}: {}]".format(precision(), tests))

    for h in [id3,cart,c45]:
        print("\n"+h.__name__.upper())
        data = get_data(5,11, tests, h)
        plt.plot([x[0] for x in data], [x[1] for x in data], label=h.__name__)

    plt.legend()
    if save:
        fname = "h_performance_line.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def h_performance_bar1(save=True):
    def get_data(xs, tests, heuristic):
        current = 0
        for _ in range(tests):
            tt = tt_gen(xs, int((2**xs)/2))
            current += heuristic(tt).nodes_amount
        return (xs, current/tests)

    xs=12
    tests = 1000
    plt.xlabel("Heuristic")
    plt.ylabel("Tree size (nodes)")
    plt.title("[rs=(2^xs)/2, xs={}, {}: {}]".format(xs, precision(), tests))

    data = []
    for h in [id3, cart, c45]:
        print(h.__name__)
        data.append((h.__name__, get_data(xs, tests, h)[1]))
    num_data = [d[1] for d in data]
    labels = zip([d[0] for d in data], num_data)
    labels = ["{} ({})".format(l[0], round(l[1],1)) for l in labels]
    plt.bar(labels, num_data, color=["blue", "orange", "green"])

    if save:
        fname = "h_performance_bar1.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def h_performance_bar2(save=True):
    def get_data(xs, tests, heuristic):
        current = 0
        for _ in range(tests):
            tt = tt_gen(xs, int((2**xs)/10))
            current += heuristic(tt).nodes_amount
        return (xs, current/tests)

    xs=12
    tests = 10000
    plt.xlabel("Heuristic")
    plt.ylabel("Tree size (nodes)")
    plt.title("[rs=(2^xs)/10, xs={}, {}: {}]".format(xs, precision(), tests))

    data = []
    for h in [id3, cart, c45]:
        print(h.__name__)
        data.append((h.__name__, get_data(xs, tests, h)[1]))
    num_data = [d[1] for d in data]
    labels = zip([d[0] for d in data], num_data)
    labels = ["{} ({})".format(l[0], round(l[1],1)) for l in labels]
    plt.bar(labels, num_data, color=["blue", "orange", "green"])

    if save:
        fname = "h_performance_bar2.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def h_performance_bar3(save=True):
    def get_data(xs, tests, heuristic):
        current = 0
        for _ in range(tests):
            tt = tt_gen(xs, int((2**xs)/25))
            current += heuristic(tt).nodes_amount
        return (xs, current/tests)

    xs=12
    tests = 10000
    plt.xlabel("Heuristic")
    plt.ylabel("Tree size (nodes)")
    plt.title("[rs=(2^xs)/25, xs={}, {}: {}]".format(xs, precision(), tests))

    data = []
    for h in [id3, cart, c45]:
        print(h.__name__)
        data.append((h.__name__, get_data(xs, tests, h)[1]))
    num_data = [d[1] for d in data]
    labels = zip([d[0] for d in data], num_data)
    labels = ["{} ({})".format(l[0], round(l[1],1)) for l in labels]
    plt.bar(labels, num_data, color=["blue", "orange", "green"])

    if save:
        fname = "h_performance_bar3.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def h_runtime_comparison(save=True):
    def get_data(min_xs, max_xs, tests, heuristic):
        output=[]
        for xs in range(min_xs, max_xs+1):
            current = 0
            for t in range(tests):
                tt = tt_gen(xs, int((2**xs)/2))

                start = process_time()
                tree = heuristic(tt)
                end = process_time()

                current += end-start
            output.append((xs, current/tests))
            print(xs, output[-1])
        return output

    tests = 1000
    plt.xlabel("Number of attributes")
    plt.ylabel("Runtime (s)")
    plt.title("[rs=(2^xs)/2, precision: {}]".format(tests))

    for h in [id3,double_id3]:
        print("\n"+h.__name__)
        data = get_data(5,11, tests, h)
        plt.plot([x[0] for x in data], [x[1] for x in data], label=h.__name__)

    plt.legend()
    if save:
        fname = "id3_double_id3_rt.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()


def opt_runtime_comparison(save=True):
    def get_data(min_xs, max_xs, tests, heuristic):
        output=[]
        for xs in range(min_xs, max_xs+1):
            current = 0
            for t in range(tests):
                tt = tt_gen(xs, int((2**xs)/3))
                try:
                    start = process_time()
                    tree = heuristic(tt)
                    end = process_time()
                except:
                    print("error")
                    tests-=1

                current += end-start
            output.append((xs, current/tests))
            print(xs, output[-1])
        return output

    tests = 1000
    plt.xlabel("Number of attributes")
    plt.ylabel("Runtime (s)")
    plt.title("[rs=(2^xs)/3, precision: {}]".format(tests))

    for h in [id3,optimal]:
        print("\n"+h.__name__)
        data = get_data(3,6, tests, h)
        plt.plot([x[0] for x in data], [x[1] for x in data], label=h.__name__)

    plt.legend()
    if save:
        fname = "id3_optimal_rt.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()




def id3_vs_optimal(save=True):
    def get_data(min_xs, max_xs, tests, heuristic):
        output=[]
        for xs in range(min_xs, max_xs+1):
            print(xs)
            current = 0
            for _ in range(tests):
                try:
                    tt = tt_gen(xs, int((2**xs)/3))
                    current += heuristic(tt).nodes_amount
                except:
                    print("error!")
                    tests-1
            output.append((xs, current/tests))
        return output

    tests = 1000
    plt.xlabel("Number of attributes")
    plt.ylabel("Tree size (nodes)")
    plt.title("[rs=(2^xs)/3, {}: {}]".format(precision(), tests))

    for h in [id3,optimal]:
        print("\n"+h.__name__.upper())
        data = get_data(3,7, tests, h)
        plt.plot([x[0] for x in data], [x[1] for x in data], label=h.__name__)

    plt.legend()
    if save:
        fname = "id3_vs_optimal.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def id3_vs_topdown(save=True):
    def get_data(min_xs, max_xs, tests, heuristic):
        output=[]
        for xs in range(min_xs, max_xs+1):
            print(xs)
            current = 0
            for _ in range(tests):
                tt = tt_gen(xs, int((2**xs)/2))
                current += heuristic(tt).nodes_amount
            output.append((xs, current/tests))
        return output

    tests = 1000
    plt.xlabel("Number of attributes")
    plt.ylabel("Tree size (nodes)")
    plt.title("[rs=(2^xs)/2, {}: {}]".format(precision(), tests))

    for h in [id3,topdown]:
        print("\n"+h.__name__.upper())
        data = get_data(4,12, tests, h)
        l = h.__name__
        if l=="topdown":
            l="worst_case"
        plt.plot([x[0] for x in data], [x[1] for x in data], label=l)

    plt.legend()
    if save:
        fname = "id3_vs_topdown.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def id3_misclassification(save=True):
    def get_data(min_xs, max_xs, tests, heuristic):
        output=[]
        for xs in range(min_xs, max_xs+1):
            print("\nxs={}".format(xs))
            misses = 0
            opt_ratios = 0
            errors = 0
            for t in range(tests):
                print(t)
                tt = tt_gen(xs, int((2**xs)/4))
                try:
                    opt_roots = [t.root.value for t in gen_optimal(tt)]
                    misses += not heuristic(tt).root.value in opt_roots
                    opt_ratios += len(opt_roots)/count_trees(tt)
                except:
                    tests -= 1
                    errors += 1
            print("errors: {}".format(errors))
            output.append((xs, 100*misses/tests, 100*opt_ratios/tests))

        return output

    tests = 100
    plt.xlabel("Number of attributes")
    plt.ylabel("Percentage of total")
    plt.title("[rs=(2^xs)/4, precision: {}]".format(tests))

    for h in [id3]:
        print("\n"+h.__name__)
        data = get_data(4,6, tests, h)
        plt.plot([x[0] for x in data], [x[1] for x in data], label=" % of {} splits made on correct attribute".format(h.__name__))
        plt.plot([x[0] for x in data], [x[2] for x in data], label="% of trees optimal ")

    plt.legend()
    if save:
        fname = "id3_misclassification.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()

def id3_vs_double_id3(save=True):
    def get_data(min_xs, max_xs, tests, heuristic):
        output=[]
        for xs in range(min_xs, max_xs+1):
            print(xs)
            current = 0
            for _ in range(tests):
                tt = tt_gen(xs, int((2**xs)/2))
                current += heuristic(tt).nodes_amount
            output.append((xs, current/tests))
        return output

    tests = 1000
    plt.xlabel("Number of attributes")
    plt.ylabel("Tree size (nodes)")
    plt.title("[rs=(2^xs)/2, {}: {}]".format(precision(), tests))

    for h in [id3,double_id3]:
        print("\n"+h.__name__.upper())
        data = get_data(5,11, tests, h)
        plt.plot([x[0] for x in data], [x[1] for x in data], label=h.__name__)

    plt.legend()
    if save:
        fname = "double_id3.png"
        plt.savefig(save_dir() + fname)
        print(fname + " saved.")
    else:
        plt.show()
    plt.close()




### CHAPTER 5: MODELS ###
## helpers ##
def data_dir():
    return "data/"

def export_data(filename, x_label, y_label, data):
    f = open('{}.csv'.format(data_dir()+filename), 'w')
    output = "{},{}".format(x_label, y_label)
    for r in data:
        output += "\n{},{}".format(r[0], r[1])
    f.write(output)
    f.close()


def model1(xs, rs, a, b):
    return a*rs*((math.exp(b)/2)**xs)

def pct_dif(truth, value):
    return 100*abs(value-truth)/truth


## data ##
def heuristic_training_gen(save=True):
    def get_data(rs_array, xs, tests, heuristic):
        output=[]
        max_rs = 2**xs
        for rs in rs_array:
            print(rs, max_rs)
            current = 0
            for _ in range(tests):
                tt = tt_gen(xs, rs)
                current += heuristic(tt).nodes_amount
            output.append((rs, current/tests))
        return output

    for h in [id3, c45, cart, topdown]:
        for xs in range(5, 15+1):
            tests = 300
            step = 0.05
            rs_array = [int((2**xs)*x) for x in np.arange(0+step,(1+step)/3,step) if int((2**xs)*x)!=0]
            data = get_data(rs_array, xs, tests, h)
            export_data("tree growth with rs growth [{}, xs={}]".format(h.__name__, xs), "rows", "tree size (xs={})".format(xs), data)

## data ##
def optimal_training_gen(save=True):
    def get_data(rs_array, xs, tests, heuristic):
        print("xs="+str(xs))
        output=[]
        max_rs = 2**xs
        for rs in rs_array:
            print(round(100*rs/(max_rs/3), 0), "%")
            current = 0
            for _ in range(tests):
                tt = tt_gen(xs, rs)
                try:
                    current += heuristic(tt).nodes_amount
                except:
                    tests=-1
                    f = open(data_dir()+"fails.txt", 'a')
                    f.write(str(tt))
                    f.close()
            output.append((rs, current/tests))
        return output

    h = optimal
    for xs in range(6,8):
        tests = 200
        step = 0.05
        rs_array = [int((2**xs)*x) for x in np.arange(0+step,(1+step)/3,step) if int((2**xs)*x)!=0]
        data = get_data(rs_array, xs, tests, h)
        export_data("tree growth with rs growth [{}, xs={}]".format(h.__name__, xs), "rows", "tree size (xs={})".format(xs), data)

def topdown_comp(save=True):
    def f(a, b, xs, rs):
        return a*rs*((math.exp(b)/2)**xs)
    

    fig = plt.figure(figsize = (12,10))
    ax = plt.axes(projection='3d')

    fakelines = []
    labels = []
    for a, b in [(1.58, 0.7), (1, 0.78)]:   
        xs = np.arange(3, 6.1, 0.1)
        rs = np.arange(3, 6.1, 0.1)

        Xs, Rs = np.meshgrid(xs, rs)
        F = f(a,b,Xs, Rs) 

        ax.plot_surface(Xs, Rs, F) # cmap = plt.cm.cividis)
        ax.set_label("test")
        # Set axes label
        ax.set_xlabel('xs', labelpad=20)
        ax.set_ylabel('rs', labelpad=20)
        ax.set_zlabel('n', labelpad=20)
        fakelines.append(mpl.lines.Line2D([0],[0], linestyle="none", c='b', marker = 'o'))
        labels.append('a={}, b={}'.format(a,b))
        # fig.colorbar(surf, shrink=0.5, aspect=8)
    
    ax.legend(fakelines, labels, numpoints = 1)
    leg = ax.get_legend()
    leg.legendHandles[0].set_color('orange')
    leg.legendHandles[1].set_color('blue')

    plt.show()

def coeffs1_eval(save=True):
    alg_as = [(topdown, 1.58), (id3, 1.02), (c45, 1.02), (cart, 1.02)]
    b = 0.7
    

    tests = 10000
    output = "\ntests: {}\n".format(tests)
    for (alg, a) in alg_as:
            fails=0
            count = 0
            print(alg.__name__)
            for i in range(tests):
                if i%1000==0:
                    print(i)
                xs = randint(3,15)
                rs = randint(1, round((2**xs)/3))
                # print("xs:{}, rs:{}".format(xs, rs))
                try:
                    truth = alg(tt_gen(xs, rs)).nodes_amount
                    count+= pct_dif(truth,model1(xs, rs, a, b))
                except:
                    fails +=1
                    tests -=1
            count/=tests
            output += "{}: {}% [fails:{}]\n".format(alg.__name__, count,fails)
    if save:
        f = open(save_dir() + "model1_eval.txt", 'a')
        f.write(output)
        f.close()
    else:
        print(output)

def coeffs2_eval(save=True):
    alg_bs = [(topdown, 0.78), (id3, 0.72), (c45, 0.71), (cart, 0.71), (optimal,0.65)]
    a = 1

    tests = 10000
    output = "\ntests: {}\n".format(tests)
    for (alg, b) in alg_bs:
            fails=0
            relative = 0
            absolute = 0
            print(alg.__name__)
            for i in range(tests):
                if i%1000==0:
                    print(i)
                xs = randint(3,6)
                rs = randint(1, round((2**xs)/3))
                # print("xs:{}, rs:{}".format(xs, rs))
                try:
                    truth = alg(tt_gen(xs, rs)).nodes_amount
                    model = model1(xs, rs, a, b) 
                    relative+= pct_dif(truth,model)
                    absolute+= abs(truth-model)
                except:
                    fails +=1
                    tests -=1
            relative/=tests
            absolute/=tests
            output += "{}: {}%, {} nodes [fails:{}]\n".format(alg.__name__, relative, absolute ,fails)
    if save:
        f = open(save_dir() + "model2_eval.txt", 'a')
        f.write(output)
        f.close()
    else:
        print(output)




### CHAPTER 1: INTRODUCTION ###
# comparison_tt()
# comparison_tree()

### CHAPTER 2: BACKGROUND ###
# truth_table()
# small_tree()
# medium_tree()
# big_tree()

### CHAPTER 3: ALGORITHMS ###
# uc_tt()
# uc_tree()

### CHAPTER 4 EXPERIMENTS ###
# rel_row_increase()
# abs_row_increase()
# h_performance_line()
# h_performance_bar1()
# h_performance_bar2()
# h_performance_bar3()
# h_runtime_comparison()
# opt_runtime_comparison()
# id3_vs_topdown()
# id3_vs_optimal()
# id3_misclassification()
# id3_vs_double_id3()

### CHAPTER 5: MODELS ###
# heuristic_training_gen()
# optimal_training_gen()
# topdown_comp()
# coeffs1_eval()
# coeffs2_eval()

print("done")
