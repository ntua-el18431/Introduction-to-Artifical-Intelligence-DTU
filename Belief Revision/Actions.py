from Extras import *
from AndFormula import AndFormula
from OrFormula import OrFormula

def contraction(bBase, contractor, type_of_priority : str ):
    if type_of_priority == "Length":
        bBase = list(bBase).sort(key = len(Formula.get_variables))   #-->Priority based on number of variables in clause. NEEDS CHECK
    elif type_of_priority == "Time":
        bBase = list(bBase)
        newBase = []
        cBeliefBase = convert(NotFormula(contractor))                   #Add the negation of the contractor in out current contracted belief Base. cBeliefBase is the "and" of all the clauses in the current contracted belief base
        for i in bBase:                                                  #For every element i of our initial belief Base
            if AndFormula(cBeliefBase,i).dicts_that_satisfy({}) != []:        #If there is a world in which the current contracted belief base can co-exist with i
                newBase.append(i)                                               #then add i to our new belief base
                cBeliefBase = AndFormula(cBeliefBase, i)                        #and add i to our current contracted belief Base
    return newBase


def expansion(bBase, expander):
    new_expander = convert(expander)                    #We keep everything in our belief Base in CNF and formated
    or_clauses = split_and([],new_expander)             #Format all the or_clauses that make-up the CNF of the new_expander
    formated_or = []
    for i in or_clauses:                                #for every element i in the or_clauses set
        formated_or.append(format_or(i))                #format i and add to the formated_or set
    new_expander = format_and(and_everything(formated_or)) #"and" all the clauses in the formated_or set and format the resulting clause. This is now the new expander

    if entailment_check_truth_table(bBase,new_expander):   #Check if the new_expander is entailed from our belief Base
        return bBase                                          #If it is return the belief Base

    return bBase.append(new_expander)                       #Else add the new expander to the belief Base


def revision(bBase, revisioner):                                   #Revision using Levi's identity
    contracted = contraction(bBase, NotFormula(revisioner))
    if (entailment_check_truth_table(contracted,revisioner)):        #If the revisioner is entailed from our belief Base
        return contracted                                                 #return the belief Base
    return expansion(contracted, revisioner)


def entailment_check(bBase, clause2):       #Entailment check using resolution algorithm (slides 9 p.15) 
    if (bBase == []):
        return False
    and_bBase = convert(AndFormula(and_everything(bBase),NotFormula(clause2)))      #convert beliefBase ∧ (¬clause2) into CNF
    clauses = set(split_and([],and_bBase))                                          #Retrieve resulting clauses
    while(len(clauses) != 0):                                               #Until there are no more clauses that can produce a new clause via resolution
        first = clauses.pop()                                               #Pop a clause out of the clauses set
        to_add = set()
        for i in clauses:                                                   #For every element i in the clauses set
            result = format_or(OrFormula(first,i))                          #Perform resolution of i and the popped element
            if result.compare_in_cnf(Variable("1")):                         #If the result is an empty clause
                return True                                                       #return true
            exists = False
            for j in clauses | to_add:                                       #If the result is in the clauses set
                if j.compare_in_cnf(result):
                    exists = True
                    break                                                         #Continue to the next element
            if not exists:                                                    #Else add to clauses set
                to_add.add(result)
        clauses |= to_add
    return False


def entailment_check_truth_table(bBase, clause):         #Entailment check using a version of truth table method. 
        if (bBase == []):
            return False
        new_me = AndFormula(and_everything(bBase), NotFormula(clause))       #Construct beliefBase ∧ (¬clause)
        variables = list(new_me.get_variables())  
        length = len(variables)
        end_goal = 2 ** length
        result = []

        for j in range(0, end_goal):                   #Get all possible combinations of truth values of the variables. If p1,p2,p3 are the truth values of the variables, treat p1p2p3 as a binary integer.
            new_dict = {}
            for i in range(length):                    #For all the digits of the binary integer
                digit = (j & (  
                            1 << i)) >> i            # Get the value of the digit (Source: https://stackoverflow.com/questions/49079440/access-an-element-of-a-binary-number-in-python)
                new_dict[variables[i]] = bool(digit)         #Match the value of the digit with the truth value of the variable to which it corresponds

            if new_me.truth_evaluation(new_dict) == True:        #If for this valuation beliefBase ∧ (¬clause) is satisfied
                return False                                              # Entailment is False
        return True