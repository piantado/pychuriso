"""A Python implementation of churiso and binary lambda calculus

Options:
Usage:
    run.py [-v | --verbose] [--search-basis=<combinators>] [--show-gs] [--max-depth=<int>] [--max-find=<int>] [--no-order] [--input=<string>]

    -v --verbose                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: SKI].
    --show-gs                     Show the auxiliary gs variables
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 20].
    --max-find=<int>              Exit if you find this many combinators [default: 300].
    --no-order                    Do not re-order the constraints
    --input=<string>              The name of the input file
"""

from run import *


if __name__ == "__main__":
    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.001")
    condition = 0
    MAX_FIND = int(arguments['--max-find'])
    combos = [arguments['--search-basis']]

    if condition==0 or 2 or 4 or 6:
        generalizations = [ ['f', 'a'], ['f', 'b']]
    elif(condition==1):
        generalizations = [['f', 'a'], ['f', 'b'], ['f', 'c']]


    # print a header
    print "condition nsolution basis generalization length runtime answer"
    # run through all the possible combinations of combinators oh geeze what a tongue twister
    for c in combos:
        print "# Starting on: " + c

        for condition in [0,1,2,3,4,5,6,7]:
            basis = basis_from_argstring(str(c))

            symbolTable, variables, uniques, facts, shows = {}, [], [], [], []  # initialize
            load_source(arguments['--input'] % condition, symbolTable, uniques, facts, shows, basis)  # modifies the arguments

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

                    # each condition has a different "novel", "never-before-seen" object
                    if len(equalset) == 0:
                        if condition == 0  or 4 or 6:
                            equalset = {'c'}
                        if condition ==3:
                            equalset={'e'}
                        else:
                            equalset = {'d'}

                    print condition, nsolution, solution, c,''.join(g), l, rc, "'%s'" % ''.join(sorted(equalset))
                    #with open(arguments['--output'], 'a') as f:
                        #print >> f, condition, nsolution, c, ''.join(g), l, rc, "'%s'" % ''.join(sorted(equalset))