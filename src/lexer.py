import ply.lex as lex

reserved = {
    'class': 'CLASS',
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'int': 'INT_TYPE',
    'String': 'STRING_TYPE'
}

tokens = list(reserved.values()) + [
    # Literales y operadores
    'IDENTIFIER', 'NUMBER', 'STRING_LITERAL', 
    'PLUS', 'MINUS', 'MULT', 'DIV', 
    'EQUALS', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'SEMICOLON', 'DOT',   
    'EQUALSBOOL'
]

def t_IDENTIFIER(t):
    r'[a-zA-Z_$][a-zA-Z0-9_$]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check si es palabra reservada
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remover comillas
    return t

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_EQUALSBOOL = r'=='
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_DOT = r'\.'

t_ignore = ' \t'  # Ignorar espacios y tabs

def t_COMMENT(t):
    r'(//.*)|(/\*(.|\n)*?\*/)'
    pass  # Ignorar comentarios

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()


def analizar(codigoStr):
    lexer.input(codigoStr)
    resultado = ""
    for tok in lexer:
        resultado += f"Token: {tok.type}, Valor: {tok.value}, Linea: {tok.lineno}\n"
    return resultado