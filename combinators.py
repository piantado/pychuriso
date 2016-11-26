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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the combinator basis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def basis_from_argstring(s):
    """
    This parses the string of combinators that we will search over. We can either include a combinator defined in terms of SK
    (thus penalizing length/complexity in that way) or as a primitive itself. The convention is that combinators you
    wish to define in terms of SK should be followed by "sk" (case sensitive). So SKIskBskCW will include I And B in terms
    of SK, but C and W was primitives themselves
    """
    basis = []
    for cstr, c, sk in re.findall("(([A-Z])(sk)?)", s):
        if sk == 'sk':
            basis.append(combinator2program[c])
        elif sk == '':
            basis.append(c)
        else:
            raise Exception("Bad sk type in combinator string: "+cstr)

    return basis

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enumeration of combinators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def combinators_at_depth_uncached(d, basis, normal=True):
    if d == 0:
        for c in basis:
            yield c
    else:
        for di in xrange(d): # go 0..(d-1)
            # print ">>", di, d-di
            for x in combinators_at_depth(di, basis, normal):
                if normal and not is_normal_form(x): continue

                for y in combinators_at_depth(d-1-di, basis, normal):
                    if normal and not is_normal_form(y): continue

                    s = '.'+x+y

                    if normal and not is_normal_form(s):
                        continue
                    else:
                        yield s


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
                l = list(combinators_at_depth_uncached(d, basis, normal))
                combinator_cache[k] = l
                for c in l:
                    yield c



def all_combinators(basis, max_depth=9999, **kwargs):
    for d in xrange(max_depth):
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

