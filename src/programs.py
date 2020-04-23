"""

Manipulation routines for programs (sequences of combinators)

"""
import scipy
from math import log

class NoCloseException(Exception):
    """ Raised when a program subexpression does not close before the end of the string (for some reason)"""
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Manipulat ASK strings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def find_close(s,pos=0):
    # print "Finding close: ", s, pos
    nopen = 0
    for i in xrange(pos,len(s)):
        if s[i] == '.':
            if nopen == 0: # start of strings, applications create two gaps (don't fill one)
                nopen += 2
            else:
                nopen += 1
        else:
            nopen -= 1

        if nopen <= 0:
            return i

    raise NoCloseException

def tostring(s, start=0):
    if(s[start] == '.'):
        pos1 = find_close(s,start+1)
        return "(%s %s)" % (tostring(s,start+1), tostring(s,pos1+1))
    else:
        return s[start]

def is_normal_form(s):
    """
    Assuming the right number of elements in the string, it is normal form if these substrings don't occur
    NOTE: seems faster than string.find
    TODO: We should recompile this into a regex instead of a bunch of string matches
    """

    return ("..K" not in s) and   \
           ("...S" not in s) and  \
           (".I" not in s) and    \
           ("....E" not in s) and \
           ("..T" not in s) and   \
           (".M" not in s) and    \
           ("...B" not in s) and  \
           ("...C" not in s) and  \
           ("..W" not in s)



def next_chunk(s, start):
    """ Return a substring of the next complete combinator found and its final position """
    end = find_close(s, start)
    return s[start:end+1], end

def count_leaves(x):
    return len(re.sub(r"\.", "", x))

def catalan_prior(x, basis):
    """ Choose a length from l ~ exponential(1) and then a tree from that length. Returns log probability """
    l = count_leaves(x)
    return -log(l) - log_catalan_number(l-1) - l * log(len(basis))

def log_catalan_number(n):
    return log(scipy.special.comb(2*n,n)) - log(n+1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse partheses into ASK string
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConversionException(Exception):
    pass

class NoCloseException(ConversionException):
    pass

class NoOpenException(ConversionException):
    pass


def find_close_parens(s, pos=0, count=0):
    if pos >= len(s):
        raise NoCloseException
    elif s[pos] == "(":
        return find_close_parens(s, pos + 1, count + 1)
    elif s[pos] == ")":
        if count > 1:
            return find_close_parens(s, pos + 1, count - 1)
        elif count == 1:
            return pos
        else:
            raise NoOpenException
    else:
        return find_close_parens(s, pos + 1, count)


import re


def find_term(s, pos=0):
    if s[pos:] == "":
        return (pos, pos, '')
    elif s[pos] == ")":
        raise NoOpenException
    elif s[pos] in ' \t\n\r\f\v':
        return find_term(s, pos + 1)
    elif s[pos] == "(":
        end = find_close_parens(s, pos=pos) + 1
        return (pos, end, s[pos:end])
    else:
        m = re.compile('[^\s()]+').match(s[pos:])
        return (pos + m.start(), pos + m.end(), s[(pos + m.start()):(pos + m.end())])


def rebracket(s):
    # empty terms
    if s == '':
        return ''

    # collect all the terms

    terms = []
    pos = 0
    while pos < len(s):
        _, pos, term = find_term(s, pos)
        terms += [term] if term else []

    # rebracket each term as needed
    niceterms = [rebracket(t[1:-1]) if (t[0] == '(' and t[-1] == ')') else t
                 for t in terms]

    # rebracket the overall term
    while len(niceterms) > 1:
        niceterms = ['(' + niceterms[0] + ' ' + niceterms[1] + ')'] + niceterms[2:]

    # return the final term
    return niceterms[0]


def fromstring(s):
    if s == "":
        return s

    sPrime = rebracket(s)

    if sPrime[0] == "(":
        xStart, xEnd, xTerm = find_term(sPrime, pos=1)
        yStart, yEnd, yTerm = find_term(sPrime, pos=(xEnd + 1))
        return '.' + fromstring(xTerm) + fromstring(yTerm)
    else:
        return sPrime[0:]
