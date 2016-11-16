

import ply.lex as lex

tokens = ['LP', 'RP', 'LB', 'RB', 'SYM', 'EQ', 'NEQ', 'ASSN', 'COMMA']

reserved = {
    'variable' : 'VARIABLE_KW',
    'unique'   : 'UNIQUE_KW',
    'show'     : 'SHOW_KW',
    'in'       : 'IN'
}
tokens += reserved.values()

t_ignore  = ' \t'

t_LB = r'\{'
t_RB = r'\}'
t_LP = r'\('
t_RP = r'\)'
t_EQ =   r'='
t_NEQ = r'\!='
t_ASSN = r':='
t_COMMA = r','

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
