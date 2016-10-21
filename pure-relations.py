"""A Python implementation of churiso and binary lambda calculus

Options:
Usage:
    run.py <input> [-v | --verbose] [--search-basis=<combinators>] [--show-gs] [--max-depth=<int>] [--max-find=<int>] [--no-order]

    -v --verbose                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: ISKBC].
    --show-gs                     Show the auxiliary gs variables
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 20].
    --max-find=<int>              Exit if you find this many combinators [default: 10000].
    --no-order                    Do not re-order the constraints
"""


from SimpleFact import SimpleFact
from run import *


if __name__ == "__main__":
    #do all our conditions
    for i in range(0,5):
        from docopt import docopt
        arguments = docopt(__doc__, version="pychuriso 0.001")

        arguments['<input>']="domains/PureRelations/condition"+str(i)+".txt"
        defines, variables, uniques, facts, shows = parse_source(arguments['<input>'])

        # Set the search basis
        import combinators
        combinators.set_search_basis(arguments['--search-basis'])

        # set up the starting solution
        start = dict()
        for d, v in defines.items(): start[d] = v  # add the defines
        for v in variables:         start[v] = v  # variables have themselves as values, already asserted to be single chars

        # test out the ordering of facts
        if not arguments['--no-order']:
            facts = order_facts(start, facts)
            print "# Best fact ordering: yielding score %s" % compute_complexity(defines, facts), facts
        else:
            print "# Running with fact ordering %s" % compute_complexity(defines, facts), facts

        MAX_FIND = int(arguments['--max-find'])

        generalizations = [SimpleFact('a', 'a', '=', '*show*'),
                           SimpleFact('a', 'b', '=', '*show*'),
                           SimpleFact('b', 'a', '=', '*show*'),
                           SimpleFact('b', 'b', '=', '*show*'),
                           SimpleFact('a', 'c', '=', '*show*'),
                           SimpleFact('c', 'a', '=', '*show*'),
                           SimpleFact('c', 'b', '=', '*show*'),
                           SimpleFact('c', 'c', '=', '*show*'),
                           ]

        with open('/home/Jenna/Desktop/PureRelations/outputwE.csv', 'a') as f:
            # Now do the search
            for which, solution in enumerate(search(start, facts, uniques, int(arguments['--max-depth']), show=arguments['--verbose'])):

                l  =  sum(len(v) for v in solution.values())
                rc = get_reduction_count(solution, facts)

                print "#", l, rc, solution

                for gi, g in enumerate(generalizations):
                    d = deepcopy(solution)
                    try:
                        update_defines(d, [g])
                    except ReductionException:
                        d['*show*'] = 'NON-HALT'
                    equalset = {k for k in d.keys() if d[k] == d['*show*']} - {'*show*', 'I'}
                    if len(equalset) == 0:
                        equalset = {'d'}


                    print>> f, i,which, gi, l, rc, g.f+g.x, ''.join(equalset)