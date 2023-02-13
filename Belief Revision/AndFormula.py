from Formula import Formula

# Implements binary and

class AndFormula(Formula):
    def __init__(self, p1: Formula, p2: Formula):
        super().__init__(p1, p2)

    @property
    def formula_type(self):
        return "And"

    def truth_evaluation(self, dict):
        return self.p1.truth_evaluation(dict) and (self.p2.truth_evaluation(dict))

    def get_variables(self):
        return self.p1.get_variables() | self.p2.get_variables()

    def get_variables_wn(self):
        return self.p1.get_variables_wn() | self.p2.get_variables_wn()

    def __str__(self):
        return "(" + str(self.p1) + ") ∧ (" + str(self.p2) + ")"

    def __repr__(self):
        return "(" + str(self.p1) + ") ∧ (" + str(self.p2) + ")"

    #We assume CN Form.
    #Returns a set of frozen sets. Each frozen set includes all the Variables(as tuples) appearing in one or clause of the CNF.
    def get_or_clauses(self):
        if self.p1.formula_type != "And" and self.p2.formula_type != "And":
            return {frozenset(self.p1.get_variables_wn()) , frozenset(self.p2.get_variables_wn())}
        if self.p1.formula_type != "And":
            return {frozenset(self.p1.get_variables_wn())} | self.p2.get_or_clauses()
        if self.p2.formula_type != "And":
            return {frozenset(self.p2.get_variables_wn())} | self.p1.get_or_clauses()
        return self.p1.get_or_clauses() | self.p2.get_or_clauses()
