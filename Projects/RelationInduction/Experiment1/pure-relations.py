"""A Python implementation of churiso

Options:
Usage:
    run.py [-v | --verbose] [--search-basis=<combinators>] [--show-gs] [--max-depth=<int>] [--max-find=<int>] [--no-order] [--output=<string>] [--input=<string>] [--f]

    -v --verbose                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: ISKBC].
    --show-gs                     Show the auxiliary gs variables
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 12].
    --max-find=<int>              Exit if you find this many combinators [default: 10000].
    --no-order                    Do not re-order the constraints
    --output=<string>             The name of the output file
    --input=<string>              The name of the input file
    --f                           Are we finding f with abcd as variables?
"""

from run import *


if __name__ == "__main__":
    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.001")
    MAX_FIND = int(arguments['--max-find'])
    c = arguments['--search-basis']
    
    generalizations = [ ['a', 'a'], ['a', 'b'], ['a','c'], ['b', 'a'], ['b', 'b'], ['b','c'], ['c', 'a'], ['c', 'b'], ['c','c']]

    if arguments['--f']:
        assert 'f' in arguments['--input'], "Are you sure you have the right input file?"
        generalizations = [ [['f','a'], 'a'], [['f','a'], 'b'], [['f','a'],'c'], [['f','b'], 'a'], [['f','b'], 'b'], [['f','b'],'c'], [['f','c'], 'a'], [['f','c'], 'b']]

    # print a header
    print "condition nsolution basis generalization length runtime answer"

    # run through all the possible combinations of combinators oh geeze what a tongue twister

    print "# Starting on: " + c

    for condition in [0,1,2,3,4]:
        basis = basis_from_argstring(str(c))

        symbolTable, variables, uniques, facts, shows = {}, [], [], [], []  # initialize
        load_source( arguments['--input'] % condition, symbolTable, uniques, facts, shows, basis)  # modifies the arguments

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

                print condition, nsolution, solution, c, ''.join(str(g)), l, rc, "'%s'" % ''.join(sorted(equalset))
                #with open(arguments['--output'], 'a') as f:
                    #print >> f, condition, nsolution, c, ''.join(g), l, rc, "'%s'" % ''.join(sorted(equalset))
