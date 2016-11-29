"""A Python implementation of churiso and binary lambda calculus

Options:
Usage:
    run.py <input> [-v | --verbose] [--search-basis=<combinators>] [--show-gs] [--max-depth=<int>] [--max-find=<int>] [--no-order] [--output=<string>]

    -v --verbose                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: ISKBC].
    --show-gs                     Show the auxiliary gs variables
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 20].
    --max-find=<int>              Exit if you find this many combinators [default: 10000].
    --no-order                    Do not re-order the constraints
    --output=<string>             The name of the output file
"""


from SimpleFact import SimpleFact
from run import *


if __name__ == "__main__":
    import itertools
    nators = "SKITBMWCE"
    combos = []
    for l in range(0,len(nators)+1):
        for v in itertools.combinations(list(nators),l):
            combos.append(str(''.join(v)))
    combos.remove('')
    print combos[0]
    print type(combos[0])
    # run through all the possible combinations of combinators oh geeze what a tongue twister
    for c in combos:
        print "Starting on: " + c
        #do all our conditions
        for i in range(0,5):
            from docopt import docopt
            arguments = docopt(__doc__, version="pychuriso 0.001")

            arguments['<input>']="domains/PureRelations/condition"+str(i)+".txt"
            defines, variables, uniques, facts, shows = parse_source(arguments['<input>'])

            # Set the search basis
            import combinators
            combinators.set_search_basis(str(c))

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

            with open('/home/Jenna/Desktop/PureRelations/Rscripts/'+arguments['--output']+ str(c) + '.csv', 'a') as f:
                # Now do the search
                from combinators import set_search_basis
                set_search_basis(c)
                for which, solution in enumerate(search(start, facts, uniques, int(arguments['--max-depth']),show=arguments['--verbose'])):

                    l  =  sum(len(v) for v in solution.values())
                    rc = get_reduction_count(solution, facts)

                    #print "#", l, rc, solution
                    #print arguments['--search-basis']

                    for gi, g in enumerate(generalizations):
                        d = deepcopy(solution)
                        try:
                            update_defines(d, [g])
                        except ReductionException:
                            d['*show*'] = 'NON-HALT'
                        equalset = {k for k in d.keys() if d[k] == d['*show*']} - {'*show*', 'I'}
                        if len(equalset) == 0:
                            if i == 4:
                                equalset = {'d'}
                            else:
                                equalset = {'c'}


                        print>> f, i,which, gi, l, rc, g.f+g.x, ''.join(equalset)