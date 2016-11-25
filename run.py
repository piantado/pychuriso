"""A Python implementation of churiso and binary lambda calculus

Options:
Usage:
    pychuriso.py <input> [-v | --trace] [--search-basis=<combinators>] [--not-normal-form] [--condensed] [--max-depth=<int>] [--max-find=<int>] [--no-order]

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
from copy import deepcopy
import reduction
from parser import load_source
from FactOrder import compute_complexity, order_facts
from combinators import substitute

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

        if k in variables:
            assert v==k
            continue

        assert k in defines or is_normal_form(v)
        print "%s := %s" % (k, tostring(v))

    for s, sf in shows:
        try:
            r = reduce_combinator(substitute(sf, solution))
        except ReductionException:
            r = 'NON-HALT'

        equalset = [k for k in solution.keys() if solution[k] == r]  # which of our defines is this equal to?

        print "show %s -> %s == {%s}" % (s, tostring(r), ', '.join(equalset))

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
        print nc,

    # and show the shows
    for s, sf in shows:
        d = deepcopy(solution)
        try:
            r = reduce_combinator(substitute(sf, solution))
        except ReductionException:
            r = 'NON-HALT'

        equalset = [k for k in solution.keys() if solution[k] == r] # which of our defines is this equal to?
        print "\"%s\"" % ','.join(list(equalset)),

    print "\n",

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":

    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.002")

    # Set the search basis (must happen before parsing or else it overwrites "add" keywords)
    import combinators
    combinators.set_search_basis(arguments['--search-basis'])

    defines, variables, uniques, facts, shows =  load_source(arguments['<input>'])

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

