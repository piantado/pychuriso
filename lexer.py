

import ply.lex as lex

tokens = ['LP', 'RP', 'SYM', 'EQ', 'NEQ', 'PEQ', 'ASSN', 'OR', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA']

reserved = {
    'forall'   : 'FORALL_KW',
    'unique'   : 'UNIQUE_KW',
    'add'      : 'ADD_KW',
    'show'     : 'SHOW_KW',
    'in'       : 'IN',
    'not'      : 'NOT'
}
tokens += reserved.values()

t_ignore  = ' \t'

t_LP = r'\('
t_RP = r'\)'
t_EQ =   r'='
t_NEQ = r'\!='
t_ASSN = r':='
t_PEQ  = r'\~='
t_OR = r'\|'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# Define symbols, anything allowed in an S-expressionn
def t_SYM(t):
    r'([a-zA-Z0-9_\-\$\*\#\@\?]+)'

    # in case we try to match a SYM as a reserved, fix it!
    # see http://stackoverflow.com/questions/5022129/ply-lex-parsing-problem
    if t.value in reserved:
        t.type = reserved[t.value]

    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])

lexer = lex.lex()
