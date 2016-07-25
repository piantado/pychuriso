

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
