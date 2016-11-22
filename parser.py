import ply.yacc as yacc

from lexer import tokens

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Each line of source
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def p_line(p):
    """ line : fact
             | forall_statement
             | define_statement
             | unique_statement
             | show_statement"""
    # print "Line:", list(p)
    p[0] = p[1]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Keywords
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def p_forall_statement(p):
    """ forall_statement : FORALL_KW symlist"""
    for a in p[2]:
        assert len(a) == 1, "*** Variables must be single characters %s" % a

    p[0] = ('forall', p[2])

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
# Base combinator rules
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def p_fact(p):
    """fact : struct EQ struct
            | struct NEQ struct
            | struct PEQ struct
            | struct IN LBRACE fact_set RBRACE
            | NOT fact
            | LBRACKET fact RBRACKET
            | fact OR fact """
    if p[2] == '=':
        p[0] = EqualityFact(make_left_binary(p[1]), make_left_binary(p[3]))
    elif p[2] == '!=':
        p[0] = InEqualityFact(make_left_binary(p[1]), make_left_binary(p[3]))
    elif p[2] == '~=':
        p[0] = PartialEqualityFact(make_left_binary(p[1]), make_left_binary(p[3]))
    elif p[2] == 'in':
        p[0] = InFact(make_left_binary(p[1]), [make_left_binary(v) for v in p[4]])
    elif p[1] == 'not':
        assert isinstance(p[2], Fact)
        p[0] = NegationFact(p[2])
    elif p[1] == '[':
        assert isinstance(p[2], Fact)
        p[0] = p[2]
    elif p[2] == '|':
        if isinstance(p[1], Disjunction):
            p[0] = p[1]
            p[0].add(make_left_binary(p[3]))
        else:
            p[0] = Disjunction([make_left_binary(p[1]), make_left_binary(p[3])])


def p_fact_set(p):
    """ fact_set : struct
                 | fact_set COMMA struct"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_struct(p):
    """struct : SYM
              | struct struct
              | LP struct RP """
    # This returns a list of lists for a structure
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Code for handling the tree structures of combinators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from Facts import *

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

def combinator_from_binary_list(l):
    # Takes a list like ['a', ['b', 'c']] and converts to .a.bc

    if isinstance(l, list):
        assert len(l) == 2, "List must be binary!"
        return '.' + combinator_from_binary_list(l[0]) + combinator_from_binary_list(l[1])
    else:
        return l

def string_from_binary_list(l):
    if isinstance(l, list):
        assert len(l) == 2, "List must be binary!"
        return '(%s %s)' % (string_from_binary_list(l[0]), string_from_binary_list(l[1]))
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

            if isinstance(p, Fact):
                facts.append(p)
            else:
                print "#", l
                t = p[0] # first thing is the kind of line we're handling

                # and update depending on what the line is
                if t == 'define':
                    assert p[1] not in defines, "*** Duplicate define for %s " % p[1]
                    defines[p[1]] = combinator_from_binary_list(make_left_binary(p[2]))
                elif t == 'unique':
                    uniques.append( p[1] )
                elif t == 'forall':
                    variables.extend(p[1])
                elif t == 'show':

                    p1b = make_left_binary(p[1])

                    shows.append( (string_from_binary_list(p1b), p1b) )

    return defines, variables, uniques, facts, shows
