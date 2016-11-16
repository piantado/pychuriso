import ply.yacc as yacc

from lexer import tokens

def p_line(p):
    """ line : statement
             | variable_statement
             | define_statement
             | unique_statement
             | show_statement"""
    # print "Line:", list(p)
    p[0] = p[1]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Keywords
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def p_variable_statement(p):
    """ variable_statement : VARIABLE_KW symlist"""
    for a in p[2]:
        assert len(a) == 1, "*** Variables must be single characters %s" % a

    p[0] = ('variable', p[2])

def p_unique_statement(p):
    """ unique_statement : UNIQUE_KW symlist"""
    p[0] = ('unique', p[2])

def p_show_statement(p):
    """ show_statement : SHOW_KW struct"""
    p[0] = ('show', p[2])

def p_define_statement(p):
    """ define_statement : SYM ASSN struct """
    p[0] = ('define', p[1], p[3])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# List of symbols
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# a list of symbols
def p_symlist(p):
    """ symlist : SYM
                | symlist SYM """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# combinator structures
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def p_statement(p):
    """statement : struct EQ struct
                 | struct NEQ struct
                 | struct PEQ struct
                 | struct IN LB structlist RB"""

    if p[2] == '=' or p[2] == '!=':
        p[0] = ['statement', p[1], p[2], p[3]]
    else:
        assert p[2] == 'in'
        p[0] = ['statement', p[1], 'in', p[4]]

# used in the RHS of "in" operations
def p_structlist(p):
    """ structlist : struct
                   | structlist COMMA struct"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[1].append(p[3])

def p_struct(p):
    """struct : SYM
              | struct struct
              | LP struct RP """
    if len(p) == 2: # SYM
        p[0] = p[1]
    elif len(p) == 3: # struct struct
        if not isinstance(p[1], list):
            p[1] = [p[1]]

        if not isinstance(p[2], list):
            p[2] = [p[2]]

        p[0] = p[1] + p[2]
    elif len(p) == 4: # LP struct RP
       p[0] = [p[2]]
    else:
        assert False, "ERROR %s" % list(p)


def p_error(p):
    print "Syntax error in input", p

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The actual parser
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parser = yacc.yacc()

# print parser.parse("f = ((g a) (b c) d e f)")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Code for handling the tree structures of combinators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Facts import *
from misc import gensym

def make_left_binary(l):
    """
    Take a list like [a b c] and make it into a binary tree like [[a b] c]
    respecting the standard order of combinatory logic
    """
    if not isinstance(l, list):
        return l
    elif len(l) == 1: # unlist singleton lists
        return make_left_binary(l[0])
    elif len(l) == 2:
        return [make_left_binary(l[0]), make_left_binary(l[1])]
    else:
        newl = [ [make_left_binary(l[0]), make_left_binary(l[1])] ]
        newl.extend(l[2:])
        return make_left_binary(newl)


def make_facts_binary(l, to, op='=', y=None):
    """
    Take a l and decompose it into binary rules, putting them all into "to",
    with the SimpleFact using op and (f x)=y.
    """

    l = make_left_binary(l)
    f, x = l

    if isinstance(f, list):
        gs = gensym()
        make_facts_binary(f, to, '=', gs) # these must be equals
        f = gs

    if isinstance(x, list):
        gs = gensym()
        make_facts_binary(x, to, '=', gs)
        x = gs

    if op == '=':
        to.append(EqualityFact(f,x,y))
    elif op == '!=':
        to.append(InEqualityFact(f,x,y))
    elif op == '~=':
        to.append(PartialEqualityFact(f,x,y))
    else:
        assert False, "Bad fact type %s" % op

def combinator_from_binary_list(l):
    # Takes a list like ['a', ['b', 'c']] and converts to .a.bc

    if isinstance(l, list):
        assert len(l) == 2, "List must be binary!"
        return '.' + combinator_from_binary_list(l[0]) + combinator_from_binary_list(l[1])
    else:
        return l

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Code for handling the tree structures of combinators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re

def load_source(file):

    defines   = {}
    variables = []
    uniques   = []
    facts     = []
    shows     = []

    with open(file) as f:
        for l in f:
            l = l.strip() # remove whitespace
            if re.match(r"\s*#", l): continue # skip comments
            if not re.match(r"[^\s]", l): continue # skip whitespace

            p = parser.parse(l)

            t = p[0] # first thing is the kind of line we're handling
            print ">>", p


            # and update depending on what the line is
            if t == 'define':
                assert p[1] not in defines, "*** Duplicate define for %s " % p[1]
                defines[p[1]] = combinator_from_binary_list(make_left_binary(p[2]))
            elif t == 'unique':
                uniques.append( p[1] )
            elif t == 'variable':
                variables.extend(p[1])
            elif t == 'show':
                shows.append({'l':make_left_binary(p[1])})
            elif t == 'statement':
                lhs, op, rhs = p[1], p[2], p[3]

                if op == 'in':
                    print ">>", p
                    if isinstance(lhs, list):  # must make a gs for it
                        gs = gensym()
                        make_facts_binary(lhs, facts, op='=',  y=gs)
                        lhs = gs # for below

                    # now for each rhs, make a binary symbol
                    new_rhs = []
                    for r in rhs:
                        if isinstance(r, str): # just a symbol, can be stored as is
                            new_rhs.append(r)
                        else:
                            assert isinstance(rhs, list) # a structure, so define a symbol
                            gs = gensym()
                            make_facts_binary(r, facts, op='=', y=gs)
                            new_rhs.append(gs)
                    # Now make the right kind of fact
                    facts.append(InFact(lhs, new_rhs))

                elif op == '=' or op == '!=' or op == '~=':

                    if (not isinstance(lhs, list)) and (not isinstance(rhs, list)):
                        assert False, "*** Cannot have symbol equality (x=y). Use I := I, (I x) = y"

                    if not isinstance(rhs, list):
                        make_facts_binary(lhs, facts, op=op, y=rhs)
                    elif not isinstance(lhs, list):
                        make_facts_binary(rhs, facts, op=op, y=lhs)
                    else:

                        # if we are both lists, make a gensym
                        assert isinstance(lhs, list) and isinstance(rhs, list)
                        gs = gensym()
                        make_facts_binary(lhs, facts, op='=', y=gs)  # one is equal to gs
                        make_facts_binary(rhs, facts, op=op, y=gs)  # one is op-equal to gs

    return defines, variables, uniques, facts, shows
