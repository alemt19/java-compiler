import ply.lex as lex
from .tkn_rules import *
from .keywords import keywords
from .tokens import tokens

reserved = keywords
tokens = list(reserved.values()) + tokens

def t_IDENTIFIER(t):
    r'[a-zA-Z_$][a-zA-Z0-9_$]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Revisar si es palabra reservada
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remover comillas
    return t

t_ignore = ' \t'  # Ignorar espacios y tabs

def t_COMMENT(t):
    r'(//.*)|(/\*(.|\n)*?\*/)'
    pass  # Ignorar comentarios

def t_newline(t):
    r'\r?\n'  # Coincide con \n o \r\n
    t.lexer.lineno += 1

errors = []

def t_error(t):
    errors.append(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}, posición {t.lexpos}")
    t.lexer.skip(1)  # Salta el carácter ilegal

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