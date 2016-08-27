MAX_CACHE=11 # cache all combinators up to this length

# this is used for reading in the search basis
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


def combinators_at_depth_uncached(d, normal=True):
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
def combinators_at_depth(d, normal=True):
    """ enumerate all with d-1 applies. If normal, we want only normal form ones"""
    global combinator_cache
    # print combinator_cache.keys()

    if d > MAX_CACHE:
        # print "TOO BIG"
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

def check_applies(c):
    """ Make sure the condition on applies is satisfied (st the number of arguments is correct) """
    nopen = 1
    for ci in c:
        if nopen == 0: return False # cannot have anything once we hit zero

        if ci=='S':
            nopen -= 1
        elif ci == 'K':
            nopen -= 1
        elif ci == '.':
            nopen += 1 # we fill one, but we open two

        if nopen < 0: return False # cannot go below zero
    return nopen==0 # good only if we exit with no applies open


def next_combinator(c):
    """ A string-based counter for combinators. Right now, very stupid and slow """
    c = list(c)
    while True:

        for i in xrange(len(c)):
            if c[i] == 'S':
                c[i] = 'K'
                break
            elif c[i] == 'K':
                c[i] = '.'
                break
            elif c[i] == '.':
                c[i] = 'S'
                # no break, to carry

                if i == len(c)-1: # if we carry on the last
                    c =['S'] * (len(c)+1)

        if check_applies(c):
            return ''.join(c)



if __name__ == "__main__":
    #
    c = 'S'
    while True:
        print ''.join(c)
        c = next_combinator(c)
        if(len(c)) >= 14: break;

    # for c in all_combinators():
    #     # print get_depth(c), c
    #     # assert check_applies(c)
    #     print ''.join(c)
    #     if(len(c)) >= 14: break;