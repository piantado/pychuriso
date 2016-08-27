"""

The dumbest and simplest search algorithm (mainly for debugging, checking): enumerate all solutions with an increasing
depth bound that is independent on each. This is dumb because depth n solutions re-search all of depth 1...(n-1) solutions.

"""
from reduction import *
from misc import is_gensym
from combinators import all_combinators
from SimpleFact import SimpleFact
from misc import check_unique

def search_(partial, facts, unique, max_depth, show=False):
    """ Take a partial solution and some facts and enumerate the remaining solutions at this depth """

    if show: print "Searching with partial ", max_depth, ["%s:%s"% (k,tostring(v))  for k,v in partial.items()  if not is_gensym(k) ], facts[:1]

    if len(facts) == 0:
        yield partial
    else:

        f0 = facts[0]

        if f0.f not in partial:

            for v in all_combinators(max_depth=max_depth, normal=True):
                if check_unique(partial, unique, f0.f, v):
                    partial[f0.f] = v # add this and recurse
                    for s in search_(partial, facts, unique, max_depth, show=show):
                        yield s
                    del partial[f0.f]

        elif f0.x not in partial:

            for v in all_combinators(max_depth=max_depth, normal=True):
                if check_unique(partial, unique, f0.x, v):
                    partial[f0.x] = v # add this and recurse
                    for s in search_(partial, facts, unique, max_depth, show=show):
                        yield s
                    del partial[f0.x]

        elif f0.rhs in partial: # this is defined, so either accept or not depending on the op

            if f0.check(partial):
                for s in search_(partial, facts[1:], unique, depth=depth, show=show):
                    yield s


        else:
            # f0.f and f0.x are defined, but f0.partial is not, so push and recurse
            try:
                v = app(partial[f0.f], partial[f0.x])
                assert is_normal_form(v)

                if f0.op != '=':
                    raise Exception("Cannot push non-equality constraint")

                if check_unique(partial, unique, f0.rhs, v):

                    partial[f0.rhs] = v

                    for s in search_(partial, facts[1:], unique, max_depth=max_depth, show=show):
                        yield s

                    del partial[f0.rhs]

            except ReductionException:

                if f0.rhs in partial: # hmm needed? In case we get a reduction exception? O
                    del partial[f0.rhs]

                pass



from copy import deepcopy
def search(start, facts, unique, max_depth, **kwargs):
    for d in xrange(max_depth):
        print "# Increasing depth to", d
        for soln in search_(deepcopy(start), facts, unique, d, **kwargs):
            yield soln