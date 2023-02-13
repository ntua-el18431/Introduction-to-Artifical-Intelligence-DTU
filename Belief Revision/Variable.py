from Formula import Formula

# Wraperclass for variable symbols

class Variable(Formula):
    def __init__(self, p: str):
        super().__init__(p, None)

    @property
    def formula_type(self):
        return "Variable"

    def __str__(self):
        return str(self.p1)

    #Called by get_or_clauses in AndFormula
    def get_or_clauses(self):
        return {frozenset(self.get_variables_wn())}

    def __repr__(self):
        return str(self.p1)

    def get_variables_wn(self):
        return {(self.p1,1)}

    def truth_evaluation(self, dict):
        return dict[str(self)]

    def get_variables(self):
        return {str(self)}

    #Compare clauses only containing either or clauses, or variables or NotFormulas
    def compare_in_cnf(self,other):
        if (self.get_variables_wn() == other.get_variables_wn()):
            return True
        else:
            return False