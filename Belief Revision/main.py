from ast import Not
from posixpath import split
from Formula import Formula
from Variable import Variable
from AndFormula import AndFormula
from OrFormula import OrFormula
from NotFormula import NotFormula
from ImpliesFormula import ImpliesFormula
from EquivFormula import EquivFormula
from Postulates import *
from Actions import *
from Extras import *


snp = NotFormula((Variable("p")))
sp = Variable("p")
sq = Variable("q")
sr = Variable("r")
ss = Variable("s")

bBase = []

expansion(bBase,ImpliesFormula(snp,sq))
expansion(bBase,ImpliesFormula(sq,sp))
expansion(bBase,ImpliesFormula(sp,AndFormula(sr,ss)))

bBase_check = bBase.copy()
print(entailment_check_truth_table(bBase,OrFormula(OrFormula(sp,sr),ss)))


bBaseForm = and_everything(bBase)
world_belief = bBaseForm.dicts_that_satisfy({})

checked = [sp, sq]
checkedForm = and_everything(checked)

checked_belief = checkedForm.dicts_that_satisfy({})

print(dictionary_filler(world_belief,checked_belief))
