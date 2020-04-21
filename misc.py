
import collections


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
