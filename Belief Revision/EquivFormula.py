from Formula import Formula

# implementation of equivalent


class EquivFormula(Formula):
    def __init__(self, p1: Formula, p2: Formula):
        super().__init__(p1, p2)

    @property
    def formula_type(self):
        return "Equiv"

    def truth_evaluation(self, dict):
        return (self.p1.truth_evaluation(dict) and self.p2.truth_evaluation(dict)) or (
                    (not self.p1.truth_evaluation(dict)) and (not self.p2.truth_evaluation(dict)))

    def get_variables(self):
        return self.p1.get_variables() | self.p2.get_variables()

    def get_variables_wn(self):
        return self.p1.get_variables_wn() | self.p2.get_variables_wn()

    def __str__(self):
        return "(" + str(self.p1) + ") ⟷ (" + str(self.p2) + ")"

    def __repr__(self):
        return "(" + str(self.p1) + ") ⟷ (" + str(self.p2) + ")"
