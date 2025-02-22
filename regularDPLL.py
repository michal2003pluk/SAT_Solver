# Imports
import numpy as np
from collections import Counter
from itertools import chain

# Returns the next variable to branch on, which is the most common one
def getNextBranchVariable(clause_set):
    # Return the most common variable in the clause_set
    return Counter(chain.from_iterable(clause_set)).most_common(1)[0][0]

# Returns None if [] is generated during propagation
# Returns new_clause_set if propagation was successful (could be an empty clause set)
def UP(clause_set, unit_literals):
    # Return original clause_set if no unit literals to propagate over
    if not unit_literals:
        return clause_set

    # Go through each clause and create a copy of it
    new_clause_set = []
    for clause in clause_set:
        clause_copy = clause[:]
        # Check if the clause contains any unit literals
        for unit_literal in unit_literals:
            # If the unit literal is in the clause then remove the whole clause and break
            if unit_literal in clause_copy:
                clause_copy = None
                break
            # If the complemented literal is in the clause then remove the variable
            elif (-unit_literal) in clause_copy:
                clause_copy.remove(-unit_literal)

                if not clause_copy:
                    return None

        if clause_copy is not None:
            new_clause_set.append(clause_copy)
    
    return new_clause_set

# Main backtracking function
def dpll_sat_solve(clause_set, partial_assignment=[]):
    new_clause_set = clause_set

# Branching on current variable

    # If first dpll_solve recursion
    if not partial_assignment:
        # If clause set is empty then sat
        if not clause_set:
            return []
        # Check if the initial clause_set is unsatisfiable
        if [] in clause_set:
            return False
    else:
        # Branch on the last variable added to the partial assignment
        branch_clause_set=branchDPLL(clause_set, partial_assignment[-1])
        if branch_clause_set == None:
            return False
        if not branch_clause_set:
            return partial_assignment

        new_clause_set = branch_clause_set
    
# Unit propagation

    # Unit propagate with deletion
    unit_literals = set([clause[0] for clause in new_clause_set if len(clause) == 1])
    while (unit_literals):
        if containsComplementPair(unit_literals):
            return False
        new_clause_set = UP(new_clause_set, unit_literals)
        if new_clause_set is None:
            return False
        elif not new_clause_set:
            return partial_assignment
        unit_literals = set([clause[0] for clause in new_clause_set if len(clause) == 1])

    if not new_clause_set:
        return partial_assignment

    # Choose next branching variable
    nextVariable = getNextBranchVariable(new_clause_set)

# Branching to next variables

    # Branch on each truth assignment
    for literal in [nextVariable,-nextVariable]:
        # Store branch result
        result = dpll_sat_solve(new_clause_set, partial_assignment + [literal])
        # If a result was returned then it must be a solution
        if result:
            return result

    return False

# Returns None if [] is generated during branching
# Returns new_clause_set if branching was successful (could be an empty clause set)
def branchDPLL(clause_set, branchOn):
    new_clause_set = []
    
    # Go through each clause
    for clause in clause_set:
        # If the exact literal is in the clause then there is no point adding it to the new clause because it gets eliminated
        if branchOn not in clause:
            # Copy the clause
            clause_copy = clause[:]
            if (-branchOn) in clause_copy:
                clause_copy.remove(-branchOn)

                # If the clause is empty after removal then clause_set is unsat and return
                if not clause_copy:
                    return None
            
            new_clause_set.append(clause_copy)

    return new_clause_set

# Returns True if the unit literals contain a complement pair i.e {-1, 1} or {7, -7}
def containsComplementPair(literals):
    seen = set()
    # Go through each literal
    for literal in literals:
        seen.add(literal)
        # If its complement has already been seen then there is a complement pair
        if -literal in seen:
            return True
        
    # No complement pairs found
    return False


from vsdc48 import load_dimacs, check_truth_assignment
import timeit

fp = 'sat_instances/'

# clauses = load_dimacs(fp +'unsat.txt')
# clauses = load_dimacs(fp +'sat.txt')
# clauses = load_dimacs(fp +'customSAT.txt')
# clauses = load_dimacs(fp +'W_2,3_ n=8.txt')
# clauses = load_dimacs(fp +'PHP-5-4.txt')
# clauses = load_dimacs(fp +'LNP-6.txt')
# clauses = load_dimacs(fp +'gt.txt')
# clauses = load_dimacs(fp +'8queens.txt')
clauses = load_dimacs(fp + 'n=100.txt')


print(np.mean(np.array(timeit.repeat('dpll_sat_solve(clauses)', globals=globals(), number=1, repeat=1))))

# sol = dpll_sat_solve(clauses)
# print(sol)
# if sol:
#     print(check_truth_assignment(clauses, sol))