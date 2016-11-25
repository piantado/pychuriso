"""

The dumbest and simplest search algorithm (mainly for debugging, checking): enumerate all solutions with an increasing
depth bound that is independent on each. This is dumb because depth n solutions re-search all of depth 1...(n-1) solutions.

"""
from reduction import *
import combinators
from combinators import all_combinators
from Facts import *
from misc import check_unique

def search_(partial, facts, unique, max_depth, normal=True, show=False):
    """ Take a partial solution and some facts and enumerate the remaining solutions at this depth """

    if show: print "Searching with partial ", max_depth, ["%s:%s"% (k,tostring(v))  for k,v in partial.items()], facts[:1]

    if len(facts) == 0:
        # A good solution
        yield partial
    else: # otherwise keep searching

        f0 = facts[0]

        open_symbols = list(set(f0.dependents()) - set(partial.keys())) # what symbols do we need?
        # print f0, open_symbols, partial

        if len(open_symbols) == 0:
            if f0.check(partial):
                # remove the fact and go on
                for soln in search_(partial, facts[1:], unique, max_depth, normal=normal, show=show):
                    yield soln

        elif isinstance(f0, EqualityFact) and f0.can_push(partial):
            # we can push an equality constraint
            try:
                v = reduce_combinator(substitute(f0.lhs, partial))

                if check_unique(partial, unique, f0.rhs, v):

                    partial[f0.rhs] = v
                    for soln in search_(partial, facts[1:], unique, max_depth, normal=normal, show=show):
                        yield soln
                    del partial[f0.rhs]
            except ReductionException:
                if f0.y in partial:  # hmm needed? In case we get a reduction exception? O
                    del partial[f0.y]
        else:
            # define an open symbol
            s = open_symbols[0]

            for v in all_combinators(max_depth=max_depth, normal=normal):
                if check_unique(partial, unique, s, v):
                    partial[s] = v  # add this and recurse
                    for soln in search_(partial, facts, unique, max_depth, normal=normal, show=show):
                        yield soln
                    del partial[s]




from copy import deepcopy
def search(start, facts, unique, max_depth, **kwargs):
    for d in xrange(max_depth):
        print "# Increasing depth to", d
        for soln in search_(deepcopy(start), facts, unique, d, **kwargs):
            yield soln