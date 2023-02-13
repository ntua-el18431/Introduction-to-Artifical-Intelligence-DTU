from Formula import Formula

# Implements binary or formulas
# format simplify the existing formular



class OrFormula(Formula):
    def __init__(self, p1: Formula, p2: Formula):
        super().__init__(p1, p2)

    @property
    def formula_type(self):
        return "Or"

    def get_variables_wn(self):
        return self.p1.get_variables_wn() | self.p2.get_variables_wn()

    def truth_evaluation(self, dict):
        return self.p1.truth_evaluation(dict) or self.p2.truth_evaluation(dict)

    def get_variables(self):
        return self.p1.get_variables() | self.p2.get_variables()

    def __str__(self):
        return "(" + str(self.p1) + ") ∨ (" + str(self.p2) + ")"

    def __repr__(self):
        return "(" + str(self.p1) + ") ∨ (" + str(self.p2) + ")"

    #Compare clauses only containing either or clauses, or variables or NotFormulas
    def compare_in_cnf(self, other):
        if (self.get_variables_wn() == other.get_variables_wn()):
            return True
        else:
            return False


