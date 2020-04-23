"""
Routines for reduction
"""


"""
Port of binary CL algortihm to python, to allow easier exploration of different algorithms
"""

MAX_LENGTH = 200
MAX_REDUCE = 100

GLOBAL_REDUCE_COUNTER = 0 # how many reductions total have we done?

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

    NOTE: IF you update combinators implemented here, be sure to update programs.is_normal_form
    """
    iters = 0


    while True:
        stepped = False
        iters += 1 # how many reduction steps have we taken?

        end = len(s)

        for i in range(end): # each character

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

            # I = (S K K)
            if i+3<=end and s[i:i+2]=='.I': # AIx -> x
                x, xend = next_chunk(s, i+2)

                s = s[:i] + x + s[xend+1:]

                stepped = True
                break

            # H = (K I)
            if i+5<=end and s[i:i+3]=='..H': # AAHxy -> y -- a version of k that's backwards
                x, xend = next_chunk(s, i+3)
                y, yend = next_chunk(s, xend+1)

                s = s[:i] + y + s[(yend+1):]

                stepped = True
                break

            # G = ((S (K ((S S) K))) (K (K ((S S) K))))
            if i + 3 <= end and s[i:i + 2] == '.G':  # AGx -> G (gobbler!)
                    x, xend = next_chunk(s, i + 2)

                    s = s[:i] + 'G' + s[xend + 1:]

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

            # T = (C I)
            if i+5<=end and s[i:i+3]=='..T': # AATxy -> Ayx
                x, xend = next_chunk(s, i+3)
                y, yend = next_chunk(s, xend+1)

                s = s[:i] + '.' + y + x + s[(yend+1):]

                stepped = True
                break

            # M = (S I I)
            if i+3<=end and s[i:i+2]=='.M': # AMx -> Axx
                x, xend = next_chunk(s, i+2)
                y, yend = next_chunk(s, xend)

                s = s[:i] + '.' + x + x + s[(yend+1):]

                stepped = True
                break

            # B = (S (K S) K)
            if i+7<=end and s[i:i+4]=='...B': # AAABxyz -> AxAyz
                x, xend = next_chunk(s, i+4)
                y, yend = next_chunk(s, xend+1)
                z, zend = next_chunk(s, yend+1)

                s = s[:i] + '.' + x  + '.' + y + z + s[zend+1:]

                stepped = True
                break

            # C = (S (B B S) (K K))
            if i+7<=end and s[i:i+4]=='...C': # AAACxyz -> AAxzy
                x, xend = next_chunk(s, i+4)
                y, yend = next_chunk(s, xend+1)
                z, zend = next_chunk(s, yend+1)

                s = s[:i] + '..' + x + z + y + s[zend+1:]

                stepped = True
                break

            # W = (S S (S K))
            if i+5<=end and s[i:i+3]=='..W': # AAWxy -> AAxyy
                x, xend = next_chunk(s, i+3)
                y, yend = next_chunk(s, xend+1)

                s = s[:i] + '..' + x + y + y +s[(yend+1):]

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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    from .combinators import all_combinators

    '''for c in all_combinators():
        try:
            rc = reduce_combinator(c)
            print is_normal_form(c), tostring(c), "->", tostring(rc)
            assert is_normal_form(rc), "*** Reduce should have returned normal form combinators"
        except ReductionException:
            print "*ReductionException*"'''
