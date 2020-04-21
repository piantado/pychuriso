"""A Python implementation of churiso and binary lambda calculus

Options:
Usage:
    run.py [-v | --verbose] [--search-basis=<combinators>] [--show-gs] [--max-depth=<int>] [--max-find=<int>] [--no-order] [--input=<string>][--output=<string>]

    -v --verbose                  Display the search incrementally (used for debugging).
    --search-basis=<combinators>  The search basis [default: SKI].
    --show-gs                     Show the auxiliary gs variables
    --max-depth=<int>             Bound the search (note the meaning of this differs by algortihm) [default: 8].
    --max-find=<int>              Exit if you find this many combinators [default: 100].
    --no-order                    Do not re-order the constraints
    --input=<string>              The name of the input file
    --output=<string>             The name of the output file

"""

from run import *

if __name__ == "__main__":
    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.001")
    condition = 0
    MAX_FIND = int(arguments['--max-find'])

    output_data = []
    # run through all the possible combinations of combinators oh geeze what a tongue twister


    for condition in range(0,8):
        print "CONDITION IS: " +str(condition)
        #restart our step count at each condition

        if condition==3:
            generalizations = [['f', 'a'], ['f', 'b'], ['f', 'c'], [ 'f','d']]
        if (condition==1) or (condition==7) or (condition==5):
            generalizations = [['f', 'a'], ['f', 'b'], ['f', 'c']]
        if (condition==0) or (condition==2) or (condition==4) or (condition==6):
            generalizations = [ ['f', 'a'], ['f', 'b']]

        basis = basis_from_argstring(str(arguments['--search-basis']))

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
            c = sum(catalan_prior(v,arguments) for v in solution.values())

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
                    if (condition == 0) or (condition==4) or (condition==6) or (condition==5):
                        equalset = {'c'}
                    if condition ==3:
                        equalset={'e'}
                    if (condition ==1) or (condition==2) or (condition==7):
                        equalset = {'d'}

                print condition, nsolution, arguments['--search-basis'],''.join(g), c, l, rc, "'%s'" % ''.join(sorted(equalset))
                output_data.append([condition, nsolution, arguments['--search-basis'], ''.join(g), c,l, rc, "'%s'" % ''.join(sorted(equalset))])

    # print a header
    print "condition nsolution basis generalization prior length runtime answer"
    for line in output_data:
        print ' '.join(map(str,line))
        print >> open(arguments['--output'],'a'), ' '.join(map(str,line))
