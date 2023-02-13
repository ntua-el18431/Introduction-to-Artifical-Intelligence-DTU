from AndFormula import AndFormula
from OrFormula import  OrFormula
from Variable import Variable
from NotFormula import NotFormula
from Formula import Formula

#https://www.cs.jhu.edu/~jason/tutorials/convert-to-CNF.html
def convert(p: Formula) -> Formula:
    if p.formula_type == "Variable":
        return p
    elif p.formula_type == "And":
        p1 = convert(p.p1)
        p2 = convert(p.p2)
        return AndFormula(p1, p2)
    elif p.formula_type == "Or":
        p1 = convert(p.p1)
        p2 = convert(p.p2)
        l1 = split_and([], p1)
        l2 = split_and([], p2)
        f = OrFormula(l1[0], l2[0])
        for i in range(len(l1)):
            for j in range(len(l2)):
                if i != 0 or j != 0:
                    f = AndFormula(f, OrFormula(l1[i], l2[j]))
        return f
    elif p.formula_type == "Not":
        if p.p1.formula_type == "Variable":
            return p
        elif p.p1.formula_type == "Not":
            return convert(p.p1.p1)
        elif p.p1.formula_type == "And":
            return convert(OrFormula(NotFormula(p.p1.p1), NotFormula(p.p1.p2)))
        elif p.p1.formula_type == "Or":
            return convert(AndFormula(NotFormula(p.p1.p1), NotFormula(p.p1.p2)))
        elif p.p1.formula_type == "Implies":
            return convert(AndFormula(p.p1.p1, NotFormula(p.p1.p2)))
        else:
            convert(OrFormula(AndFormula(p.p1.p1, NotFormula(p.p1.p2)), AndFormula(NotFormula(p.p1.p1), p.p1.p2))) 
    elif p.formula_type == "Implies":
        return convert(OrFormula(NotFormula(p.p1), p.p2))
    else:
        return convert(OrFormula(AndFormula(p.p1, p.p2), AndFormula(NotFormula(p.p1), NotFormula(p.p2))))

#format and formula containing or clauses
def format_and(clause):
    if (clause.formula_type == 'Or'):
        return format_or(clause)
    or_clauses = clause.get_or_clauses() #Get the sets of or clauses tuples

    result_clause = []
    while (len(or_clauses)!=0): #For all or clause tuples
        or_clause_tupples = or_clauses.pop()
        or_clause = []
        for i in or_clause_tupples: #Make the tuples into Variables
            if i[1] == 1:
                or_clause.append(Variable(i[0]))
            else:
                or_clause.append(NotFormula(Variable(i[0])))
        result_clause.append(or_everything(or_clause))  #"Or" them and add them to the end result list
    return and_everything(result_clause)    #return the "and" of everything in the result list


#format nested or clauses
def format_or(clause):
    result_set = set()
    if (clause.p2 == None):
        return clause

    all_variables = clause.p1.get_variables_wn() | clause.p2.get_variables_wn() #Get all variables in the or clause (as tuples)

    while(len(all_variables)!= 0):  #For all variables
        i = all_variables.pop()
        if (i[0],not i[1]) in all_variables: #if the variable and its negation are in the variable set, remove the negation and don't use the variable in the end result
            all_variables.remove((i[0],not i[1]))
            continue

        result_set.add(i)   #add variable (as tuple) in the result_set

    clause_list = []

    if (len(result_set)==0):    #No variables(tuples) are left in the clause
        return Variable("1")

    while(len(result_set)!=0):  #Convert tuples to Variables
        i =result_set.pop()
        if (i[1] == 1):
            clause_list.append(Variable(i[0]))
        else:
            clause_list.append(NotFormula(Variable(i[0])))

    return or_everything(clause_list)   #return clause resulting from  the "or" of all Variables

#Make a new clause by performing "and" operations between all the clauses in clause_list
def and_everything(clause_list):
    new_clause_list = []
    for i in clause_list:
        new_clause_list.append(convert(i))
    result = new_clause_list.pop(0)
    while(new_clause_list != []):
        result = AndFormula(new_clause_list.pop(0),result)
    return result

#Make a new clause by performing "or" operations between all the clauses in clause_list
def or_everything(clause_list):
    result = clause_list.pop(0)
    while(clause_list != []):
        result = OrFormula(clause_list.pop(0),result)
    return result


#Get a formula in CNF and return a list of the or clauses it's composed of
def split_and(lis: list, f: Formula) -> list:
    if f.formula_type == "And":
        p1 = f.p1
        p2 = f.p2
        lis = split_and(lis, p1)
        return split_and(lis, p2)
    else:
        lis.append(f)
        return lis
