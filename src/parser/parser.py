import ply.yacc as yacc
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from .sym_table import *
from .rules import *
import logging

logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()



# Manejo de errores

errores_sint = []

def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en la línea {p.lineno}, token: {p.value}"
        errores_sint.append(error_msg)
        p.lexer.skip(1)
    else:
        errores_sint.append("Error de sintaxis: fin de archivo inesperado")

def parse_code(parser, code, lexer):
    ast = parser.parse(code, lexer=lexer)
    print(get_ast_str(ast))
    symbol_table.print_table()
    if (ast):
        return get_ast_str(ast)
    else:
        return "Error en el análisis"
    
def crear_parser(tokens):
    tokens = tokens
    return yacc.yacc(debug=True, errorlog=log)

def get_errores_sint(parser):
    print(errores_sint)
    erroresStr = "\n".join(errores_sint)
    while(len(errores_sint)!= 0):
        errores_sint.pop(-1)
    parser.lineno = 1
    return erroresStr 