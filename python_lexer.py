import ply.lex as lex

keywords = {
    'int', 'float', 'char', 'void', 'if', 'else', 'for', 'while',
    'return', 'break', 'continue'
}

tokens = [
    'ID', 'INT_LITERAL', 'FLOAT_LITERAL', 
    'CHAR_LITERAL', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'INCREMENT', 'DECREMENT',
    'EQUAL', 'NOT_EQUAL',
    'LESS', 'LESS_EQUAL',
    'GREATER', 'GREATER_EQUAL',
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN',
    'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'MOD_ASSIGN',
    'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA'
] + [kw.upper() for kw in keywords]

t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_MOD           = r'%'
t_ASSIGN        = r'='

t_INCREMENT     = r'\+\+'
t_DECREMENT     = r'--'

t_EQUAL         = r'=='
t_NOT_EQUAL     = r'!='
t_LESS          = r'<'
t_LESS_EQUAL    = r'<='
t_GREATER       = r'>'
t_GREATER_EQUAL = r'>='

t_PLUS_ASSIGN   = r'\+='
t_MINUS_ASSIGN  = r'-='
t_TIMES_ASSIGN  = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN    = r'%='

t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACE        = r'\{'
t_RBRACE        = r'\}'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_SEMICOLON     = r';'
t_COMMA         = r','

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_COMMENT_LINE(t):
    r'//.*'
    pass

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    return t

def t_CHAR_LITERAL(t):
    r"'([^'\\]|\\.)'"
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

def t_error(t):
    print(f"Erro léxico: caractere inválido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
