from Formula import Formula

# implementation of implication


class ImpliesFormula(Formula):
    def __init__(self, p1: Formula, p2: Formula):
        super().__init__(p1, p2)

    @property
    def formula_type(self):
        return "Implies"

    def truth_evaluation(self, dict):
        return (not self.p1.truth_evaluation(dict)) or (self.p2.truth_evaluation(dict))

    def get_variables(self):
        return self.p1.get_variables() | self.p2.get_variables()

    def get_variables_wn(self):
        return self.p1.get_variables_wn() | self.p2.get_variables_wn()

    def __str__(self):
        return "(" + str(self.p1) + ") → (" + str(self.p2) + ")"

    def __repr__(self):
        return "(" + str(self.p1) + ") → (" + str(self.p2) + ")"
