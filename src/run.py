"""A Python implementation of churiso

Options:
Usage:
    pychuriso.py <input> [-v | --trace] [--search-basis=<combinators>] [--normal-form] [--condensed] [--show-original-basis] [--max-depth=<int>] [--max-find=<int>] [--no-order]

    -t --trace                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: ISK].
    --show-original-basis         Display and measure performance in the original basis, not SK basis
    --show-gs                     Show the auxiliary gs variables
    --condensed                   Give condensed output
    --normal-form                 Search only ove rthose in normal form -- NOTE if you do this, setting the combinator basis may not help since some combinators will never/rarely yield normal form terms and thus will be pruned out.
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 20].
    --max-find=<int>              Exit if you find this many combinators [default: 1000].
    --no-order                    Do not re-order the constraints
"""

import sys
import re
from search.block import search
from reduction import tostring,  reduce_combinator, ReductionException
from copy import deepcopy
import reduction
from parsing import load_churiso_sourcefile
from Facts import PartialEqualityFact
from FactOrder import compute_complexity, order_facts
from combinators import substitute, make_solution_sk, combinator2program
from programs import catalan_prior, fromstring

TOTAL_SOLUTION_COUNT = 0

def get_reduction_count(soln, facts):
    """ How many total reductions does it take? NOTE: This runs in the sk basis, regardless of search """

    # We are going to ignore reduction count if we contain any ~= facts
    # this way, when we sort by runtime+complexity, we just do complexity for partial reduction facts
    ## NOTE: in the future maybe we can not count these
    if(any(isinstance(f,PartialEqualityFact) for f in facts)):
        return 0

    start = reduction.GLOBAL_REDUCE_COUNTER
    for f in facts:
        q = f.check(soln), f  # run all of the applies
        if(not q): assert False

    return reduction.GLOBAL_REDUCE_COUNTER - start

def get_length(soln):
    return sum(len(v) for v in list(soln.values()))

def display_winner(arguments, defines, solution, facts, shows):
    """ Display a solution. This is zero-delimited so we can sort -z, with run times and lengths at the top """

    print("################################################################################")
    global TOTAL_SOLUTION_COUNT

    # defaulty we convert solution to sk for performance evals
    if not arguments['--show-original-basis']:
        solution = make_solution_sk(solution)

    print(TOTAL_SOLUTION_COUNT, get_length(solution), get_reduction_count(solution,facts), sum(catalan_prior(x, basis) for x in list(solution.values())))

    #version where we use catalan prior
    # print TOTAL_SOLUTION_COUNT, sum(catalan_prior(v, basis) for v in solution.values()), sum(len(v) for v in solution.values()), get_reduction_count(solution, facts)

    for k, v in list(solution.items()):
        print("%s := %s" % (k, tostring(v)))  #,  "\t# ", v

    for s, sf in shows:
        try:
            r = reduce_combinator(substitute(sf, solution))
        except ReductionException:
            r = 'NON-HALT'

        equalset = [k for k in list(solution.keys()) if solution[k] == r]  # which of our defines is this equal to?

        print("show %s -> %s == {%s}" % (s, tostring(r), ', '.join(equalset)))

    print("\0")
    sys.stdout.flush()


def condensed_display(arguments, defines, solution, facts, shows):
    """
        A single-line output, of the type that might be used for grammar inference
        This prints out the solution unmber, total length, reduction count, counts for a bunch of combinators
        then followed by the symbols each show equals
    """
    global TOTAL_SOLUTION_COUNT
    print(TOTAL_SOLUTION_COUNT, sum(len(v) for v in list(solution.values())), get_reduction_count(solution, facts), end=' ')

    # next get the counts of each combinator
    for c in 'SKIBCWETM':
        nc = sum([v.count(c) for v in list(solution.values())])
        print(nc, end=' ')

    # and show the shows
    for s, sf in shows:
        d = deepcopy(solution)
        try:
            r = reduce_combinator(substitute(sf, solution))
        except ReductionException:
            r = 'NON-HALT'

        equalset = [k for k in list(solution.keys()) if solution[k] == r] # which of our defines is this equal to?
        print("\"%s\"" % ','.join(list(equalset)), end=' ')

    print("\n", end=' ')
    sys.stdout.flush()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":

    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.01")

    # Set the search basis (must happen before parsing or else it overwrites "add" keywords)
    basis = list(arguments['--search-basis'])

    symbolTable, variables, uniques, facts, shows = {}, [], [], [], [] # initialize
    load_churiso_sourcefile(arguments['<input>'], symbolTable, uniques, facts, shows, basis) # modifies the arguments

    # test out the ordering of facts
    if not arguments['--no-order']:
        facts = order_facts(symbolTable, facts)
        print("# Best fact ordering: yielding score %s" % compute_complexity(symbolTable, facts), facts)
    else:
        print("# Running with fact ordering %s" % compute_complexity(symbolTable, facts), facts)

    sys.stdout.flush()

    MAX_FIND = int(arguments['--max-find'])

    # Now do the search
    print("# Using search basis ", basis)
    for solution in search(symbolTable, facts, uniques, int(arguments['--max-depth']), basis, normal=arguments['--normal-form'], show=arguments['--trace']):
        if arguments['--condensed']:
            condensed_display(arguments, symbolTable, solution, facts, shows)
        else:
            display_winner(arguments, symbolTable, solution, facts, shows)

        if TOTAL_SOLUTION_COUNT >= MAX_FIND:
            break

        TOTAL_SOLUTION_COUNT += 1

