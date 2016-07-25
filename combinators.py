MAX_CACHE=15 # cache all combinators up to this length

combinator2program = {'S':'S',
                      'K':'K',
                      'I':'..SKK',
                      'B':'..S.KSK',
                      'C':'..S.K..S.K..SS.KKKS'}

SEARCH_BASIS = ['S', 'K'] # what we use to search for combinators

from programs import is_normal_form

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the combinator basis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def set_search_basis(combinators):
    global SEARCH_BASIS

    SEARCH_BASIS = [combinator2program[c] for c in combinators]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enumeration of combinators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def combinators_at_depth_uncached(d, normal=False):
    if d == 0:
        for c in SEARCH_BASIS:
            yield c
    else:
        for di in xrange(d): # go 0..(d-1)
            # print ">>", di, d-di
            for x in combinators_at_depth(di, normal):
                if normal and not is_normal_form(x): continue

                for y in combinators_at_depth(d-1-di, normal):
                    if normal and not is_normal_form(y): continue

                    s = '.'+x+y

                    if normal and not is_normal_form(s):
                        continue
                    else:
                        yield s


combinator_cache = dict()
def combinators_at_depth(d, normal=False):
    """ enumerate all with d-1 applies. If normal, we want only normal form ones"""
    global combinator_cache
    # print combinator_cache.keys()

    if d > MAX_CACHE:
        print "TOO BIG"
        for c in combinators_at_depth_uncached(d,normal):
            yield c

    else:
        try:
            # first try the cache
            for c in combinator_cache[(d,normal)]:
                yield c

        except KeyError:

            # otherwise, cache and return
            if d <= MAX_CACHE:
                l = list(combinators_at_depth_uncached(d,normal))
                combinator_cache[(d,normal)] = l
                for c in l:
                    yield c



def all_combinators(max_depth=9999, **kwargs):
    for d in xrange(max_depth):
        for c in combinators_at_depth(d, **kwargs):
            yield c

def get_depth(c):
    """ What depth would c have been enumerated on? """
    return (len(c)-1)/2


if __name__ == "__main__":

    for c in all_combinators():
        print get_depth(c), c