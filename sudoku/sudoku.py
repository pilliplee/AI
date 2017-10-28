import sys
from CSP import CSP
from copy import deepcopy

#############################################################################
# ac3() - algorithm for checking arc-consistency in csp data structure
# Return: boolean
#
def ac3(csp):
    queue = list(csp.C)
    while (len(queue)>0):
        c = queue[0]
        queue.remove(c)
        x_i = c.pop()
        x_j = c.pop()
        if(revise(csp,x_i,x_j)):
            if((len(csp.D[csp.X.index(x_i)])==0) or (len(csp.D[csp.X.index(x_j)])==0)):
                return False
            if(len(csp.D[csp.X.index(x_i)])>1):
                neighbors = csp.get_neighbors(x_i)
                neighbors.remove(x_j)
                for x_k in neighbors:
                    queue.append(set([x_k,x_i]))
            elif(len(csp.D[csp.X.index(x_j)])>1):
                neighbors = csp.get_neighbors(x_j)
                neighbors.remove(x_i)
                for x_k in neighbors:
                    queue.append(set([x_k,x_j]))
    return True

#############################################################################
# revise() - update the domain of one variable by excluding the domain value
#            from the other variable
# Return: boolean
#
def revise(csp,x_i,x_j): #returns true iff we revise the domain of X_i
    revised = False
    d_i = csp.D[csp.X.index(x_i)]
    d_j = csp.D[csp.X.index(x_j)]
    if(len(d_i) == 1 and d_i <= d_j):
        d_j = d_j - d_i
        csp.D[csp.X.index(x_j)] = d_j
        revised = True
    elif(len(d_j) == 1 and d_j <= d_i):
        d_i = d_i - d_j
        csp.D[csp.X.index(x_i)] = d_i
        revised = True
    return revised

#############################################################################
# backtrack() - algorithm to search for solution and add to assignment
# Return: assignment or False
#
def backtrack(assignment,csp):
    if(csp.is_complete(assignment)):
        return assignment
    x = mrv(assignment,csp)
    csp_orig = deepcopy(csp)
    for v in csp.D[csp.X.index(x)]:
        inferences = {}
        if(csp.is_consistent(x,v)):
            assignment[x] = v
            inferences = forward_check(assignment,csp,x,v)
            if isinstance(inferences,dict):
                assignment.update(inferences)
                result = backtrack(assignment,csp)
                if isinstance(result,dict):
                    return result
        del assignment[x]
        if isinstance(inferences,dict):
            for i in inferences:
                del assignment[i]
        csp = deepcopy(csp_orig)
    return False

#############################################################################
# mrv() - minimum-remaining-value (MRV) heuristic
# Return: the variable from amongst those that have the fewest legal values
#
def mrv(assignment,csp):
    unassigned_x = {}
    index = 0
    for d in csp.D:
        if(len(d) > 1):
            unassigned_x[csp.X[index]] = len(d)
        index += 1
    sorted_unassigned_x = sorted(unassigned_x, key=unassigned_x.get)
    for x in sorted(unassigned_x, key=unassigned_x.get):
        if(x not in assignment):
            return x
    return False

#############################################################################
# forward() - implement Inference finding in the neighbor variables
# Return: dict of inferences
#
def forward_check(assignment,csp,x,v):
    inferences = {}
    neighbors = csp.get_neighbors(x)
    for n in neighbors:
        s = csp.D[csp.X.index(n)]
        if(len(s) > 1 and v in s):
            s = s - set([v])
            csp.D[csp.X.index(n)] = s
            if(len(s) == 1 and n not in assignment):
                inferences[n] = list(s)[0]
        inf_list = inferences.values()
        for inf in inf_list:
            if(inf_list.count(inf)>1):
                return False
    return inferences

#############################################################################
# main() - sudoku solver main process
# Return: void
#
def main(filename):
    csp = CSP(filename)
    if(ac3(csp)):
        if(csp.is_solved()):
            print ("Sudoku Solved!")
            csp.print_game()
        else:
            assignment = backtrack({},csp)
            if isinstance(assignment,dict):
                csp.assign(assignment)
                print ("Sudoku Solved!")
                csp.print_game()
            else:
                print ("No solution exists")
    else:
        print ("No solution exists")
