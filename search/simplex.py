"""

This fixes the length of *all* combinators to sum to a given value (depth). This prevents re-searching old solutions

NOTE: The only thing that counts against our combinator length is combinators that have been searched (via all_combinators),
not those that have been pushed

NOTE: This is still inefficient because it re-searches early strings

"""

from reduce import *
from misc import is_gensym
from combinators import combinators_at_depth, get_depth
from SimpleFact import SimpleFact, compute_complexity
from misc import check_unique


def search_(partial, facts, unique, depth, show=False):
    """ Take a partial solution and some facts and enumerate the remaining solutions at this depth """

    if show: print "Searching with partial ", depth, ["%s:%s"% (k,tostring(v))  for k,v in partial.items()  if not is_gensym(k) ], facts[:1]

    if len(facts) == 0:
        yield partial
    elif depth >= 0:

        f0 = facts[0]

        rem = compute_complexity(partial, facts)  # If we have nothing else to search over, we must be at depth exactly

        assert rem>0 or depth==0 # should never have rem=0 and depth=0 in simplex search
        # print "REM=", rem

        if f0.f not in partial:

            # if rem==1, we just filled it up with f0.f, so we require exactly this depth
            for d in ([depth] if rem == 1 else xrange(depth+1)):
                for v in combinators_at_depth(d, normal=True):
                    if check_unique(partial, unique, f0.f, v):
                        # print "Setting %s := %s" % (f0.f, v)
                        partial[f0.f] = v # add this and recurse
                        for s in search_(partial, facts, unique, depth - d, show=show):
                            yield s
                        del partial[f0.f]

        elif f0.x not in partial:

            # if rem==1, we just filled it up with f0.x, so we require exactly this depth
            for d in ([depth] if rem == 1 else xrange(depth+1)):  # we have to do this instead of all_combinators b/c we need the depth, which may not agree with get_depth in our SEARCH_BASIS
                for v in combinators_at_depth(d, normal=True):
                    if check_unique(partial, unique, f0.x, v):
                        # print "Setting %s := %s" % (f0.x, v)

                        partial[f0.x] = v # add this and recurse
                        for s in search_(partial, facts, unique, depth - d, show=show):
                            yield s
                        del partial[f0.x]

        elif f0.rhs in partial: # this is defined, so either accept or not depending on the op
            # print "Checking (%s %s) ?= %s" % (f0.f, f0.x, f0.rhs)

            if f0.check(partial):
                for s in search_(partial, facts[1:], unique, depth=depth, show=show):
                    yield s

        else:
            # f0.f and f0.x are defined, but f0.rhs is not, so push and recurse

            if f0.op == '=':

                try:
                    v = apply(partial[f0.f], partial[f0.x])

                    if check_unique(partial, unique, f0.rhs, v):
                        # print "Pushing %s := %s" % (f0.rhs, v)

                        partial[f0.rhs] = v

                        for s in search_(partial, facts[1:], unique, depth=depth, show=show):
                            yield s

                        del partial[f0.rhs]

                except ReductionException:
                    pass
                    # if f0.rhs in partial: # hmm needed? In case we get a reduction exception? O
                    #     del partial[f0.rhs]

            elif f0.op == '!=':
                raise Exception("Cannot push non-equality constraint")
            elif f0.op == '~=':  #partial eval
                try:
                    v = apply(partial[f0.f], partial[f0.x])
                except ReductionException as r:
                    v = r

                if check_unique(partial, unique, f0.rhs, v):
                    # print "Pushing %s := %s" % (f0.rhs, v)

                    partial[f0.rhs] = v

                    for s in search_(partial, facts[1:], unique, depth=depth, show=show):
                        yield s

                    del partial[f0.rhs]


from copy import deepcopy
def search(start, facts, unique, max_depth, **kwargs):
    for d in xrange(max_depth+1):
        print "# Increasing depth to", d
        for soln in search_(deepcopy(start), facts, unique, d, **kwargs):
            yield soln