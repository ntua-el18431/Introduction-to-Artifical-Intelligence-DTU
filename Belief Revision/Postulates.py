from Extras import *
from Formula import Formula
from Actions import *

def dictionary_filler(set_of_dict_1,set_of_dict_2):              #used in consequence set to help with the comparison of two lists of dictionaries by filling the dictionaries of one list with the keys missing
    keys_1 = set_of_dict_1[0].keys()                             #take the keys of the first list of dicts
    keys_2 = set_of_dict_2[0].keys()                             #take the keys of the second list of dicts
    for key in keys_1:                                           #for every key in the first list
        helper_list = []
        if key not in keys_2:                                    #if it is not in the second list
            for i in set_of_dict_2:                              #create a copy of the second list
                helper_list.append(i.copy())
            for dict in range(len(set_of_dict_2)):
                set_of_dict_2[dict][key] = True                  #in the original copy, add the the key with True value in every dictionary
                helper_list[dict][key] = False                   #in the copy, add the key with the False value in every dictionary
            set_of_dict_2 = set_of_dict_2 + helper_list          #merge the two lists
            
    return set_of_dict_2 

def in_consequence_set(believeBase, checked):                      #check if checked is in the Cn(believeBase)
    formula = and_everything(believeBase)
    worlds_check = checked.dicts_that_satisfy({})                  #worlds that satisfy the checked
    worlds_belief = formula.dicts_that_satisfy({})                 #worlds that satisfy the belief base
    worlds_check_pumped = dictionary_filler(worlds_belief, worlds_check)
    for i in worlds_belief:                                        # take a dictionary that satisfies the belief base
        flag = False                                               # initalize the flag as False
        for j in worlds_check_pumped:                              # take a dictionary that satisfies the checked
            if all(item in j.items() for item in i.items()):       # if everything that exists in the belief base dictionary also exists in the checked dictionary
                flag = True                                        # then the the belief base dictionary is a 
                break
        if flag == False:
            return False
    return True

def success_postulate(contracted, contractor):                     #prove that phi not in Cn(bBase contracted by phi)
    if in_consequence_set({}, contractor):                         #if it is a tautlogy return True
        return True                                                
    else:                                                           #if every item that exists in the contracted's world, exists also in the contractor's world
        return not in_consequence_set(contracted, contractor)       #thus proving that the contract's world is not a superset of the contracted's                                                              
                                                                    


def inclusion_postulate(bBase, contractor):
    new_base = contraction(bBase,contractor) 
    for i in new_base:                                         # check if the new_base is a subest of the original Belief Base
        if i not in bBase:
            return False
    return True


def vacuity_postulate(bBase, contractor):
    if in_consequence_set(bBase, contractor):                 #check whether phi is in consequence set of belief base
        return True                                           #if yes, terminate
    if set(bBase) != set(contraction(bBase, contractor)):     #if not, check if belief base changed
         return False                                         #if yes, return False
    return True                                               #otherwise, test holds up
    


def extensionality_postulate(bBase, contractor, contractor_friend):                     # phi # psi
    dicts_contractor = contractor.dicts_that_satisfy({})                                #worlds that satisfy phi
    dicts_contractor_friend = contractor_friend.dicts_that_satisfy({})                  #worlds that satify psi

    if in_consequence_set({}, contractor):
        return True
    if dicts_contractor == dicts_contractor_friend:                                     #if the worlds that satisfy phi and psi are the same, then phi and psi are equivalent
        if contraction(bBase, contractor) != contraction(bBase, contractor_friend):     #if they are equivalent, check whether the result of the contraction of bBase with phi and of the contraction of bBase with psi are the same
            return False
    return True



