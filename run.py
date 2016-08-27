"""A Python implementation of churiso and binary lambda calculus

Usage:
    pychuriso.py <input> [-v | --verbose] [--search-basis=<combinators>] [--show-gs] [--max-depth=<int>] [--max-find=<int>] [--no-order]

Options:
    -v --verbose                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: ISKBC].
    --show-gs                     Show the auxiliary gs variables
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 20].
    --max-find=<int>              Exit if you find this many combinators [default: 10000].
    --no-order                    Do not re-order the constraints
"""

from search.simplex import search
from parser import parse_source
from reduction import tostring,  update_defines, ReductionException
from programs import is_normal_form
from misc import is_gensym
from copy import deepcopy
from SimpleFact import compute_complexity

from random import shuffle

TOTAL_SOLUTION_COUNT = 0


def get_reduction_count(soln, facts):
    """ How many total reductions does it take? """

    start = reduce.GLOBAL_REDUCE_COUNTER
    for f in facts:
        f.check(soln) # run all of the applies
    return reduce.GLOBAL_REDUCE_COUNTER - start

def display_winner(partial, variables, facts, shows):
    """ Display a solution. This is zero-delimited so we can sort -z, with run times and lengths at the top """

    print "################################################################################"
    global TOTAL_SOLUTION_COUNT

    # confirm all constraints
    print TOTAL_SOLUTION_COUNT, sum(len(v) for v in partial.values()), get_reduction_count(partial, facts)

    print "# ---------- In SK basis ----------"
    for k, v in solution.items():

        if is_gensym(k) and not arguments['--show-gs']:
            continue

        if k in variables:
            assert v==k
            continue

        assert is_normal_form(v)
        print "%s := %s" % (k, tostring(v))

    for s, f in shows.items():
        d = deepcopy(partial)
        try:
            update_defines(d, f)
        except ReductionException:
            d['*show*'] = 'NON-HALT'

        equalset = {k for k in d.keys() if d[k]==d['*show*']}- {'*show*'} # which of our defines is this equal to?

        print "show %s -> %s == {%s}" % (s, tostring(d['*show*']), ', '.join(equalset) )

    print "\0"

    TOTAL_SOLUTION_COUNT += 1


def order_facts(start, facts):
    """ Come up with an ordering of facts. For now just greedy """

    defined = set(start.keys())
    ofacts = [] # ordered version

    while len(facts) > 0:

        # first see if we can verify any facts (thus pruning the search)
        lst = [f for f in facts if set([f.f, f.x, f.rhs]).issubset(defined) ]  # if everything is defined
        if len(lst) > 0:
            ofacts.extend(lst) # we can push them all
            for f in lst:
                facts.remove(f)
            continue

        # next see if we can push any constraints
        lst = [f for f in facts if f.op=='=' and set([f.f, f.x]).issubset(defined)]  # anything we can push
        if len(lst) > 0:
            ofacts.append(lst[0]) # only push the first, since that may permit verifying facts
            defined.add(lst[0].rhs)
            facts.remove(lst[0])
            continue

        # otherwise just pull the first fact (TODO: We can make this smart--pull facts that let us define more), pull facts that only need one f or x
        f = facts[0]
        ofacts.append(f)
        del facts[0]
        defined.add(f.f) # either it here already or we have to add it
        defined.add(f.x)
        defined.add(f.rhs)

    return ofacts

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":

    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.001")

    defines, variables, uniques, facts, shows =  parse_source(arguments['<input>'])

    # Set the search basis
    import combinators
    combinators.set_search_basis(arguments['--search-basis'])

    # set up the starting solution
    start = dict()
    for d,v in defines.items(): start[d] = v  # add the defines
    for v in variables:         start[v] = v  # variables have themselves as values, already asserted to be single chars

    # test out the ordering of facts
    if not arguments['--no-order']:
        facts = order_facts(start, facts)
        print "# Best fact ordering: yielding score %s" % compute_complexity(defines, facts), facts
    else:
        print "# Running with fact ordering %s" % compute_complexity(defines, facts), facts

    MAX_FIND = int(arguments['--max-find'])

    # Now do the search
    for solution in search(start, facts, uniques, int(arguments['--max-depth']), show=arguments['--verbose']):
        display_winner(solution, variables, facts, shows)

        if TOTAL_SOLUTION_COUNT > MAX_FIND:
            break
