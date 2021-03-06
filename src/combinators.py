MAX_CACHE=8 # cache all combinators up to this length
import re

# this is used for reading in the search basis
combinator2program = {'S':'S',
                      'K':'K',
                      'I':'..SKK',
                      'B':'..S.KSK',
                      'C':'..S..S.K..S.KSKS.KK',
                      'W':'..SS.SK',
                      'E':'E',
                      'T':'T',
                      'M':'M'}

from programs import is_normal_form
from reduction import reduce_combinator, ReductionException

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enumeration of combinators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def combinators_at_depth_uncached(d, basis, normal=False):
    """ Give back the combinators at a given depth, without caching.
        Note there is actually a bit of subtlety here. Some previous versions required
        each of the pieces to be in normal form, in order to avoid duplication,
        But it seems to be a bad idea to require s to be in normal form, because then
        we miss a lot because we can't form some long combinators that we should.
        So, here we always yield x+y, but we also reduce it first so that means sometimes
        we will have some duplicates

    """
    # NOTE That if we check normal, then we may NOT find all combinations
    # when you use terms like Bsk, because these may combine into non-normal forms

    if d == 0:
        for c in basis:
            yield c
    else:
        for di in range(d): # go 0..(d-1)
            # print ">>", di, d-di
            for x in combinators_at_depth(di, basis, normal):
                if normal and not is_normal_form(x): continue

                for y in combinators_at_depth(d-1-di, basis, normal):
                    if normal and not is_normal_form(y): continue

                    s = '.'+x+y

                    # In the past, we checked if this return was normal form; but actually
                    # this is a mistake when we have sk combinators we can't toss
                    # out non-normal stuff here because it may become non-normal
                    # once we have complex SK combinators


                    # But note, here we MUST reduce combinators, or else uniqueness is
                    # pretty weird since it doesn't require uniqueness of reduced forms.
                    # When we do this with anything other than SK basis, we might get duplicates
                    # but we can search more complex structures earlier, which is why its useful.

                    # We CAN use normal when we only have SK, since we know that we won't skip
                    # anything by being normla form

                    if normal:
                        if is_normal_form(s):
                            yield s
                        else:
                            continue
                    else:
                        try:
                            yield reduce_combinator(s)
                        except ReductionException as e:
                            pass


combinator_cache = dict()
def combinators_at_depth(d, basis, normal=True):
    """ enumerate all with d-1 applies. If normal, we want only normal form ones"""
    global combinator_cache
    # print combinator_cache.keys()

    if d > MAX_CACHE:
        for c in combinators_at_depth_uncached(d,basis, normal):
            yield c

    else:
        k = (d, tuple(basis), normal)  # how we index into the cache

        try:
            # first try the cache
            for c in combinator_cache[k]:
                yield c

        except KeyError:

            # otherwise, cache and return
            if d <= MAX_CACHE:
                l = tuple(combinators_at_depth_uncached(d, basis, normal))
                combinator_cache[k] = l
                for c in l:
                    yield c



def all_combinators(basis, max_depth=9999, **kwargs):
    for d in range(max_depth):
        for c in combinators_at_depth(d, basis, **kwargs):
            yield c

def get_depth(c):
    """ What depth would c have been enumerated on? """
    return (len(c)-1)/2


def substitute(x, defns):
    if isinstance(x, list):
        assert len(x)==2
        return '.'+substitute(x[0], defns)+substitute(x[1], defns)
    else:
        return defns.get(x,x)

def make_solution_sk(soln):
    """ This converts a solution to only sk (using combinator2program) """

    sksolution = dict()
    for symbol, comb in list(soln.items()):
        for c,p in list(combinator2program.items()): # find any defined combinator and replace it
            comb = re.sub(c,p,comb)
        sksolution[symbol] = comb
    return sksolution

