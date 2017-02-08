"""A Python implementation of churiso and binary lambda calculus

Options:
Usage:
    run.py [-v | --verbose] [--search-basis=<combinators>] [--show-gs] [--max-depth=<int>] [--max-find=<int>] [--no-order] [--output=<string>]

    -v --verbose                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: ISKBC].
    --show-gs                     Show the auxiliary gs variables
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 12].
    --max-find=<int>              Exit if you find this many combinators [default: 10000].
    --no-order                    Do not re-order the constraints
    --output=<string>             The name of the output file
"""

from run import *


if __name__ == "__main__":
    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.001")
    condition = 0
    MAX_FIND = int(arguments['--max-find'])
    combos = [arguments['--search-basis']]

    generalizations = [ ['a', 'a'], ['a', 'b'], ['a','c'], ['b', 'a'], ['b', 'b'], ['b','c'], ['c', 'a'], ['c', 'b'], ['c','c']]

    # print a header
    print "condition nsolution basis generalization length runtime answer"

    # run through all the possible combinations of combinators oh geeze what a tongue twister
    for c in combos:
        print "# Starting on: " + c

        for condition in [0,1,2,3,4]:
            basis = basis_from_argstring(str(c))

            symbolTable, variables, uniques, facts, shows = {}, [], [], [], []  # initialize
            load_source("Inputs/Exp1_nogs/condition%s.txt" % condition, symbolTable, uniques, facts, shows, basis)  # modifies the arguments

            seen = set()
            for nsolution, solution in enumerate(search(symbolTable, facts, uniques, int(arguments['--max-depth']), basis)):
                if nsolution > MAX_FIND: break

                # remove duplicates -- have to hash the dictionary
                fs = frozenset(solution.items())
                if fs in seen:
                    continue
                else:
                    seen.add(fs)

                l  =  sum(len(v) for v in solution.values())
                rc = get_reduction_count(solution, facts)

                # print solution

                for g in generalizations:

                    try:
                        r = reduce_combinator(substitute(g, solution))
                    except ReductionException:
                        r = 'NON-HALT'

                    equalset = set([k for k in solution.keys() if solution[k] == r])  # which of our defines is this equal to?
                    equalset = equalset - set({'I','gs'}) # remove I,gs since its used in our conditions but only for convenience

                    # adjust for the fact that c and d are
                    if len(equalset) == 0:
                        if condition == 4:
                            equalset = {'d'}
                        else:
                            equalset = {'c'}

                    print condition, nsolution, c, ''.join(g), l, rc, "'%s'" % ''.join(sorted(equalset))
