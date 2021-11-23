# MIT 6.034 Lab 8: Bayesian Inference
# Written by 6.034 staff

from nets import *


#### Part 1: Warm-up; Ancestors, Descendents, and Non-descendents ##############

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    anscestors = set()



    for p in net.get_parents(var):
        anscestors.update(get_ancestors(net, p))


    anscestors.update(net.get_parents(var))

    return anscestors

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    descendants = set()

    for p in net.get_children(var):
        descendants.update(get_descendants(net, p))

    descendants.update(net.get_children(var))

    return descendants

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    descendants = get_descendants(net, var)
    descendants.add(var)
    return set(net.get_variables()) - descendants


#### Part 2: Computing Probability #############################################

def simplify_givens(net, var, givens):
    """
    If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens.
    """

    if not set(net.get_parents(var)).issubset(set(givens.keys())):
        return givens

    for v in get_descendants(net, var):
        if v in givens.keys():
            return givens

    new_givens = dict(givens)
    for k in givens.keys():
        if k not in net.get_parents(var):
            del new_givens[k]

    return new_givens

    
def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"


    try:
        return net.get_probability(hypothesis, parents_vals=givens)

    except ValueError:
        try:
            givens = simplify_givens(net, list(hypothesis.keys())[0], givens)
            return net.get_probability(hypothesis, parents_vals=givens)
        except ValueError:
            raise LookupError


def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"

    product_list = []

    for var in hypothesis:

        givens = dict(hypothesis)

        for i in hypothesis:
            if i == var or i not in net.get_parents(var):
                del givens[i]

        product_list.append(probability_lookup(net, {var: hypothesis[var]}, givens))

    return product(product_list)


def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"

    sum_list = []

    for var in net.combinations(net.get_variables(), hypothesis):
        sum_list.append(probability_joint(net, var))

    return sum(sum_list)



def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"

    if not givens:
        return probability_marginal(net, hypothesis)

    # TODO make more general
    if list(hypothesis.keys())[0] == list(givens.keys())[0]:
        if hypothesis[list(hypothesis.keys())[0]] != givens[list(givens.keys())[0]]:
            return 0.0
        else:
            return 1.0

    total_dict = dict(hypothesis, **givens)

    return probability_marginal(net, total_dict)/probability_marginal(net, givens)


def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"

    if not givens:
        return probability_conditional(net, hypothesis)
    else:
        return probability_conditional(net, hypothesis, givens)


#### Part 3: Counting Parameters ###############################################

def number_of_parameters(net):
    """
    Computes the minimum number of parameters required for the Bayes net.
    """
    # product of number of values parents have, multiplied by the number of values the target has -1

    param_count_list = []

    for var in net.get_variables():
        domain = len(net.get_domain(var))

        total_parent_domain = 1
        for parent in net.get_parents(var):
            total_parent_domain = total_parent_domain * len(net.get_domain(parent))

        param_count_list.append((domain-1)*total_parent_domain)

    return sum(param_count_list)



#### Part 4: Independence ######################################################

def is_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    otherwise False. Uses numerical independence.
    """
    raise NotImplementedError
    
def is_structurally_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence).
    """
    raise NotImplementedError


#### SURVEY ####################################################################

NAME = "Theodore Calabrese"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
