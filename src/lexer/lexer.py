import ply.lex as lex
from .tkn_rules import *
from .keywords import keywords
from .tokens import tokens

reserved = keywords
tokens = list(reserved.values()) + tokens

def obtener_tokens():
    return tokens

def t_PUBLIC(t):
    r'public'
    return t

def t_PRIVATE(t):
    r'private'
    return t

def t_PROTECTED(t):
    r'protected'
    return t

def t_STATIC(t):
    r'static'
    return t

def t_CLASS(t):
    r'class'
    return t

def t_INT_TYPE(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_STRING(t):
    r'string'
    return t

# Reglas para literales

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

def t_CHARACTER_LITERAL(t):
    r'\'(\\.|[^\\\'])?\''
    t.value = t.value[1:-1]
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t):
    r'//.*'
    pass

errors = []

def t_error(t):
    errors.append(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}, posición {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

def analizar(codigoStr):
    lexer.input(codigoStr)
    resultado = ""
    for tok in lexer:
        resultado += f"Token: {tok.type}, Valor: {tok.value}, Linea: {tok.lineno}\n"
    return resultado

def errores():
    erroresStr = "\n".join(errors)
    while(len(errors)!= 0):
        errors.pop(-1)
    lexer.lineno = 1
    return erroresStr

def crear_lexer():
    return lex.lex()