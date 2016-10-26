"""
Routines for reduction
"""


"""
Port of binary CL algortihm to python, to allow easier exploration of different algorithms
"""

MAX_LENGTH = 200
MAX_REDUCE = 100

GLOBAL_REDUCE_COUNTER = 0 # how many reductions total have we done?

from combinators import SEARCH_BASIS
from programs import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define exceptions for various reduction problems
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ReductionException(Exception):
    def __init__(self, value):
        self.value = value

class RuntimeException(ReductionException):
    pass

class LengthException(ReductionException):
    pass


def reduce_combinator(s):
    """
    Reduce a string s to normal form
    """
    iters = 0

    while True: # tODO: Maybe checking whether its normal form here is faster?
        stepped = False
        iters += 1 # how many reduction steps have we taken?
        #print iters, s, tostring(s)

        ## TODO: REWRITE WITH string find for speed!
        end = len(s)

        """
        # ONLY a little faster:
        kpos = s.find("..K")
        spos = s.find("...S")

        if kpos >= 0 and (kpos<spos or spos<0) and kpos+5 <= end: # if we can do a k and its before an s
            i = kpos
            x, xend = next_chunk(s, i+3)
            y, yend = next_chunk(s, xend+1)

            s = s[:i] + x + s[(yend+1):]

            stepped = True

        elif spos >= 0 and spos >= 0 and spos+7 <= end:
            i = spos
            x, xend = next_chunk(s, i+4)
            y, yend = next_chunk(s, xend+1)
            z, zend = next_chunk(s, yend+1)

            s = s[:i] + '..' + x + z + '.' + y + z + s[zend+1:]

            stepped = True
        """
        for i in xrange(end): # each character

            if i+5<=end and s[i:i+3]=='..K': # AAKxy -> x
                x, xend = next_chunk(s, i+3)
                y, yend = next_chunk(s, xend+1)

                s = s[:i] + x + s[(yend+1):]

                stepped = True
                break

            if i+7<=end and s[i:i+4]=='...S': # AAASxyz -> AAxzAyz
                x, xend = next_chunk(s, i+4)
                y, yend = next_chunk(s, xend+1)
                z, zend = next_chunk(s, yend+1)

                s = s[:i] + '..' + x + z + '.' + y + z + s[zend+1:]

                stepped = True
                break
            if i+9<=end and s[i:i+5]=='....E': #AAAAExyab -> if x==y: a else b

                x, xend = next_chunk(s, i+5)
                y, yend = next_chunk(s, xend+1)
                a, aend = next_chunk(s, yend+1)
                b, bend = next_chunk(s, aend+1)

                if reduce_combinator(x)==reduce_combinator(y):
                    s = s[:i] + a + s[bend+1:]
                else:
                    s = s[:i] + b + s[bend+1:]

                stepped = True
                break

            if i+5<=end and s[i:i+3]=='..T': # AATxy -> yx
                x, xend = next_chunk(s, i+3)
                y, yend = next_chunk(s, xend+1)

                s = s[:i] + y + x + s[(yend+1):]

                stepped = True
                break






        if not stepped:
           break
        else:
            global GLOBAL_REDUCE_COUNTER
            GLOBAL_REDUCE_COUNTER += 1

        if len(s) > MAX_LENGTH:
            raise LengthException(s)
        if iters  > MAX_REDUCE:
            raise RuntimeException(s)

    return s

def app(f,x):
    return reduce_combinator('.'+f+x)

def update_defines(defined, facts):
    # go through the facts, pushing updates to defines
    # this is used to "eval" a complex expression
    # thus, running this and looking at the appropriate item of defined is like evaling a complex expression

    for f in facts:
        if f.op == '=': # we can only push equality constraints
            if f.rhs not in defined:
                defined[f.rhs] = app(defined[f.f], defined[f.x])
        else:
            raise Exception("Cannot have anything other than = in update defines.")

    return defined

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    from combinators import all_combinators

    '''for c in all_combinators():
        try:
            rc = reduce_combinator(c)
            print is_normal_form(c), tostring(c), "->", tostring(rc)
            assert is_normal_form(rc), "*** Reduce should have returned normal form combinators"
        except ReductionException:
            print "*ReductionException*"'''
    #
    # print reduce('AAASAASSSKK')
    # print reduce('AAASxyzww')
    # print reduce('qqAAASxyz')
    # print reduce('AAASxyz')
    #
    # print reduce('qqAAASxyzww')
    print reduce_combinator('.....SKSKxy')
    print reduce_combinator('..Kxy')
    print reduce_combinator('....E.....SKKKxy..Kxyab')
    print reduce_combinator('....E.....SKSKxy..Kxyab')
    print reduce_combinator('....E.....KxySxyzab')
    print reduce_combinator('....E.......KxySxyzKxySxyz')
    print reduce_combinator('....SS.SKxy')
    print reduce_combinator('..Txy')





