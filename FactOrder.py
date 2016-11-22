"""
Ordering of facts for search
"""
from Facts import *


def order_facts(start, facts):
    """ Come up with an ordering of facts. For now just greedy """

    defined = set(start.keys())
    ofacts = [] # ordered version

    while len(facts) > 0:

        # first see if we can verify any facts (thus pruning the search)
        lst = [f for f in facts if set(f.dependents()).issubset(defined) ]  # if everything is defined
        if len(lst) > 0:
            ofacts.extend(lst) # we can push them all
            for f in lst:
                facts.remove(f)
            continue

        # next see if we can push any constraints
        lst = [f for f in facts if isinstance(f, EqualityFact) and f.can_push(defined)]  # anything we can push
        if len(lst) > 0:
            ofacts.append(lst[0]) # only push the first, since that may permit verifying facts
            defined.add(lst[0].rhs)
            facts.remove(lst[0])
            continue

        # otherwise just pull the first fact (TODO: We can make this smart--pull facts that let us define more), pull facts that only need one f or x
        # TODO: Pick the one with the fewest dependents not in defined
        f = facts[0]
        ofacts.append(f)
        del facts[0]
        defined.update(f.dependents())

    return ofacts


def compute_complexity(defines, facts):
    """ How many remaining searches through combinators do we need?
        Our search is O(compute_complexity(defines, facts))
     """

    defined = set(defines.keys())
    cplx = 0
    for f in facts:
        # print f, f.dependents()
        if isinstance(f, EqualityFact) and f.can_push(defines):
            defined.add(f.rhs) # can push
        else:
            # we face O(dependents) search
            openset = set(f.dependents()) - defined
            cplx += len(openset)
            defined.update(openset)

    return cplx