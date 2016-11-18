
import collections

GENSYM_COUNTER = -1
def gensym():
    global GENSYM_COUNTER
    GENSYM_COUNTER += 1
    return "_gs%s"%GENSYM_COUNTER

def is_gensym(x):
    return x[:3] == "_gs"


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
