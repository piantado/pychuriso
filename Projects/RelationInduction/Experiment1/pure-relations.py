"""A Python implementation of churiso

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
    --no-gs                       Are we using the gs relationship? Eventually a more general argument here
    --funky                       Are we using the function version? e.g. a = (f a a)
"""

from run import *


if __name__ == "__main__":
    from docopt import docopt
    arguments = docopt(__doc__, version="pychuriso 0.001")
    condition = 0
    MAX_FIND = int(arguments['--max-find'])
    combos = [arguments['--search-basis']]

    #what we want: command line arguments for the following:
        # which 'relationship' function are we using? gs? something else? if using one, we write to the input file to include.
        # are we using f? if so, we need different generalizations

    def remove_gs(file):

        data = file.readlines()
        for i,line in enumerate(data):
            if "= (gs" in line:
                data[i]=""
        with open("Inputs/newcondition%s.txt" % condition, 'w+') as newfile:
            newfile.writelines(data)
        f = newfile
        return f

    def make_it_funky(file):

        data = file.readlines()
        for i,line in enumerate(data):
            if "= (gs" in line:
                data[i]=""
        with open("Inputs/newcondition%s.txt" % condition, 'w+') as newfile:
            newfile.writelines(data)
        f = newfile
        return f

    generalizations = [ ['a', 'a'], ['a', 'b'], ['a','c'], ['b', 'a'], ['b', 'b'], ['b','c'], ['c', 'a'], ['c', 'b'], ['c','c']]

    # print a header
    print "condition nsolution basis generalization length runtime answer"

    # run through all the possible combinations of combinators oh geeze what a tongue twister
    for c in combos:
        print "# Starting on: " + c

        for condition in [0,1,2,3,4]:
            f = open("Inputs/condition%s.txt" % condition,'r')
            if arguments['--no-gs']:

                f=remove_gs(f)



            basis = basis_from_argstring(str(c))

            symbolTable, variables, uniques, facts, shows = {}, [], [], [], []  # initialize
            load_source(f, symbolTable, uniques, facts, shows, basis)  # modifies the arguments

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
