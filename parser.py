"""
Parsing routines for churiso source files. NOTE: This currently only handles binary rules
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse single S-expressions, and statements (e.g. (f x) = (g (f y))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pyparsing as pp

w = pp.Word(pp.alphanums+'%_-')
lp = pp.Suppress("(")
rp = pp.Suppress(")")

sexp = pp.Forward()
sexp << (w | pp.Group(lp + pp.OneOrMore(sexp) + rp))

op = pp.Literal("=") | pp.Literal("!=")
statement = pp.Group(sexp + op + sexp)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Convert a complex s-expression into a bunch of binary ones
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from misc import gensym
from SimpleFact import SimpleFact


def treeize(l):
    """
    Take a list like [a b c] and make it into a binary tree like [[a b] c]
    respecting the standrad order of combinatory logic
    """
    if not isinstance(l, list):
        return l
    elif len(l) <= 2:
        return [treeize(l[0]), treeize(l[1])]
    else:
        newl = [[l[0], l[1]]]
        newl.extend(l[2:])
        return treeize(newl)


def binarize(l, to, op='=', y=None):
    """
    Take a l and decompose it into binary rules, putting them all into "to",
    with the SimpleFact using op and (f x)=y.
    """

    l = treeize(l)
    f, x = l

    if isinstance(f, list):
        gs = gensym()
        binarize(f, to, '=', gs) # these must be equals
        f = gs

    if isinstance(x, list):
        gs = gensym()
        binarize(x, to, '=', gs)
        x = gs

    to.append(SimpleFact(f, x, op, y))


def parse_statement(s, facts):
    """ Parse statemnets adding it to the facts """

    lhs, op, rhs = statement.parseString(s).asList()[0]

   # Defaulty we assume if there is a single symbol, it is on the right
    if not isinstance(rhs, list):
        binarize(lhs, facts, op=op, y=rhs)
    if not isinstance(lhs, list):
        binarize(rhs, facts, op=op, y=lhs)
    else:
        assert isinstance(lhs,list) and isinstance(rhs,list)
        gs = gensym()
        binarize(lhs, facts, op='=', y=gs) # one is equal to gs
        binarize(rhs, facts, op=op,  y=gs ) # one is op-equal to gs

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parse a program source file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re
from programs import fromstring

def parse_source(file):
    """ Parse an entire source file, returning defines, variables, uniques, and binarized facts """

    defines   = {}
    variables = []
    uniques   = []
    facts     = []
    shows     = dict()

    with open(file) as f:
        for l in f:
            l = l.strip() # remove whitespace
            if re.match(r"\s*#", l): continue # skip comments
            if not re.match(r"[^\s]", l): continue # skip whitespace

            r = re.match(r"\s*unique\s+([a-zA-Z0-9\s\-_]+)",l)
            if r:
                uniques.append( list(r.groups()[0].split(" ")) )
                continue

            r = re.match(r"\s*variable\s+([a-zA-Z0-9\s]+)", l)
            if r:
                v =  list(r.groups()[0].split(" "))
                assert max(len(vi) for vi in v) == 1, "*** Variables must be single characters in pychuriso"

                variables.extend( v )
                continue

            r = re.match(r"\s*show\s+([\(\)a-zA-Z0-9\s\-_]+)",l)
            if r:
                # r.groups()[0] is now an S-expression made of symbols
                # We will binarize it and store it as a new set of facts, that can
                # then be evaled in display_winner

                se = r.groups()[0]

                showfacts = []
                binarize(sexp.parseString(se)[0], showfacts, op='=', y="*show*")
                assert se not in shows, "*** Error: multiple identical shows"

                shows[se] = showfacts
                continue

            r = re.match(r"\s*([a-zA-Z0-9]+)\s*:=\s*([a-zA-Z0-9\-_\(\)\s]+)$", l)
            if r:
                defines[r.groups()[0]] = fromstring(r.groups()[1])
                continue


            # else parse
            parse_statement(l, facts)

    return defines, variables, uniques, facts, shows


if __name__ == "__main__":
    #
    # facts = []
    # parse_statement("((g f1) (f2 x1)) != (y (gg z))",facts)
    #
    # print facts
    # print op
    # print rhs

    #parse_source("domains/boolean.txt")
    # facts = []
    # print parse_statement("(t f) = (a t)", facts )

    print sexp.parseString("(is-brown (pair brown X)) ").asList()[0]

# def list2SimpleFacts(lhs, op, rhs):
#
#     def expand_side(x):
#         if len(x) <= 2:
#             return x
#         else:
#             # pull off the first element
#             x0 = x[0]
#
#             return
#
#
#
# def string2list(s):
#     """ Parse an S-expression into a list"""
#     return sexp.parseString(s).asList()