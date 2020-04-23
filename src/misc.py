
import collections
from math import log, lgamma

def check_unique(partial, unique, s, v):
    """ check whether s can equal v under the current partial and unique """

    for u in unique:
        if s in u and any(partial.get(x,None) == v for x in u):
            return False

    return True


def flatten(l):
    #http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    if isinstance(l,str):
        yield l
    else:
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, str):
                for sub in flatten(el):
                    yield sub
            else:
                yield el

def q(x):
    return "'%s'"%str(x)
def qq(x):
    return "\"%s\""%str(x)


def lfactorial(n):
    return lgamma(n+1)

def lchoose(n, k):
    return lfactorial(n) - lfactorial(k) - lfactorial(n-k)

def log_catalan_number(n):
    if n == 0: return 0
    return lchoose(2*n,n) - log(n+1)


