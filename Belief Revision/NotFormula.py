from Formula import Formula

# implementation of negation


class NotFormula(Formula):
    def __init__(self, p1: Formula):
        super().__init__(p1, "none")

    @property
    def formula_type(self):
        return "Not"

    def format(self):
        if (self.p1.formula_type == "Not"):
            return self.p1.p1
        else:
            return self

    def get_variables_wn(self):
        return {(self.p1.p1,0)}

    def truth_evaluation(self, dict):
        return not self.p1.truth_evaluation(dict)

    def get_variables(self):
        return self.p1.get_variables()

    def __str__(self):
        return "¬(" + str(self.p1) + ")"

    def __repr__(self):
        return "¬(" + str(self.p1) + ")"

    #Called by get_or_clauses in AndFormula
    def get_or_clauses(self):
        return {frozenset(self.get_variables_wn())}

    #Compare clauses only containing either or clauses, or variables or NotFormulas
    def compare_in_cnf(self,other):
        if (self.get_variables_wn() == other.get_variables_wn()):
            return True
        else:
            return False