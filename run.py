"""A Python implementation of churiso and binary lambda calculus

Options:
Usage:
    pychuriso.py <input> [-v | --trace] [--search-basis=<combinators>] [--show-gs] [--not-normal-form] [--condensed] [--max-depth=<int>] [--max-find=<int>] [--no-order]

    -t --trace                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: ISK].
    --show-gs                     Show the auxiliary gs variables
    --condensed                   Give condensed output
    --not-normal-form             Search does not require combinators to be normal form
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 20].
    --max-find=<int>              Exit if you find this many combinators [default: 10000].
    --no-order                    Do not re-order the constraints
"""

from search.block import search
from reduction import tostring,  reduce_combinator, ReductionException
from programs import is_normal_form
from misc import is_gensym
from copy import deepcopy
import reduction
from parser import load_source
from Facts import compute_complexity, EqualityFact
from combinators import substitute
from misc import flatten

TOTAL_SOLUTION_COUNT = 0

def get_reduction_count(soln, facts):
    """ How many total reductions does it take? """

    start = reduction.GLOBAL_REDUCE_COUNTER
    for f in facts:
        assert f.check(soln), f  # run all of the applies
    return reduction.GLOBAL_REDUCE_COUNTER - start

def display_winner(defines, solution, variables, facts, shows):
    """ Display a solution. This is zero-delimited so we can sort -z, with run times and lengths at the top """

    print "################################################################################"
    global TOTAL_SOLUTION_COUNT

    # confirm all constraints
    print TOTAL_SOLUTION_COUNT, sum(len(v) for v in solution.values()), get_reduction_count(solution, facts)

    # print "# ---------- In search basis ----------"
    for k, v in solution.items():

        if is_gensym(k) and not arguments['--show-gs']:
            continue

        if k in variables:
            assert v==k
            continue

        assert k in defines or is_normal_form(v)
        print "%s := %s" % (k, tostring(v))

    for s, sf in shows:
        try:
            r = reduce_combinator(substitute(sf, solution))
        except ReductionException:
            d['*show*'] = 'NON-HALT'

        equalset = [ k for k in d.keys() if d[k]==d['*show*'] and k != "*show*" and not is_gensym(k) ]# which of our defines is this equal to?

        print "show %s -> %s == {%s}" % (s, tostring(d['*show*']), ', '.join(equalset) )

    print "\0"


def condensed_display(defines, solution, variables, facts, shows):
    """
        A single-line output, of the type that might be used for grammar inference
        This prints out the solution unmber, total length, reduction count, counts for a bunch of combinators
        then followed by the symbols each show equals
    """
    global TOTAL_SOLUTION_COUNT
    print TOTAL_SOLUTION_COUNT, sum(len(v) for v in solution.values()), get_reduction_count(solution, facts),

    # next get the counts of each combinator
    for c in 'SKIBCWETM':
        nc = sum([v.count(c) for v in solution.values()])
        # print [v.count(c) for v in solution.values()]
        print nc,

    # and show the shows
    for s, sf in shows:
        d = deepcopy(solution)
        try:
            update_defines(d, sf)
        except ReductionException:
            d['*show*'] = 'NON-HALT'

        equalset = [k for k in d.keys() if d[k] == d['*show*'] and k != "*show*" and not is_gensym(k)] # which of our defines is this equal to?
        print "\"%s\"" % ','.join(list(equalset)),

    print "\n",



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
            defined.add(lst[0].y)
            facts.remove(lst[0])
            continue

        # otherwise just pull the first fact (TODO: We can make this smart--pull facts that let us define more), pull facts that only need one f or x
        # TODO: Pick the one with the fewest dependents not in defined
        f = facts[0]
        ofacts.append(f)
        del facts[0]
        defined.update(f.dependents())


    return ofacts


def update_defines(defined, facts):
    # go through the facts, pushing updates to defines
    # this is used to "eval" a complex expression
    # thus, running this and looking at the appropriate item of defined is like evaling a complex expression

    for f in facts:
        assert isinstance(f, EqualityFact)

        if f.y not in defined:
            defined[f.y] = app(defined[f.f], defined[f.x])
        else:
            assert f.y == app(defined[f.f], defined[f.x])

    return defined

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":

    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.002")

    defines, variables, uniques, facts, shows =  load_source(arguments['<input>'])

    print facts


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
    for solution in search(start, facts, uniques, int(arguments['--max-depth']), normal=not arguments['--not-normal-form'], show=arguments['--trace']):

        if arguments['--condensed']:
            condensed_display(defines, solution, variables, facts, shows)
        else:
            display_winner(defines, solution, variables, facts, shows)

        if TOTAL_SOLUTION_COUNT >= MAX_FIND:
            break

        TOTAL_SOLUTION_COUNT += 1

