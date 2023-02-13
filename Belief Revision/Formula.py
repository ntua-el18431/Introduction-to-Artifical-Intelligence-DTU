# parent class for more specific formulas.

class Formula:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @property
    def formula_type(self):
        return "Formula"

    def __str__(self):
        return "unspecified Formula"

    def __repr__(self):
        return "unspecified Formula"

    #get the truth evaluation of a formula using the truth values of the variables in dictionary dict
    def truth_evaluation(self, dict):
        return "unspecified Formula"

    #return set of variables in the clause
    def get_variables(self):
        return "unspecified Formula"

    #return set of tuples of variables in the clause. If the variable p is in a Notformula, it translates to a tuple (p,0). Otherwise it translates to a tuple (p,1)
    def get_variables_wn(self):
        return "unspecified Formula"

    #return the valuations that satisfy self, with the given truth values of variables included in the dictionary dict
    def dicts_that_satisfy(self, dict):
        left_variables = list(self.get_variables() - set(dict.keys()))          #Get all the variables whose truth value is undefined
        length = len(left_variables)
        end_goal = 2 ** length 
        result = []

        for j in range(0, end_goal):                                          #Get all possible combinations of truth values of the left variables. If p1,p2,p3 are the truth values of the left variables, treat p1p2p3 as a binary integer.
            new_dict = dict.copy()   
            for i in range(length):                                               #For all the digits of the binary integer
                digit = (j & (
                            1 << i)) >> i                                         #Get the value of the digit (Source: https://stackoverflow.com/questions/49079440/access-an-element-of-a-binary-number-in-python)
                new_dict[left_variables[i]] = bool(digit)                         #Match the value of the digit with the truth value of the variable to which it corresponds

            if self.truth_evaluation(new_dict) == True:                       #If for this caluation self is satisfied
                result.append(new_dict)                                            #Add the valuation to the result list
        return result