import ply.yacc as yacc
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lexer.lexer import tokens, crear_lexer
from sym_table import *
from rules import *

parser = yacc.yacc()

def parse_code(code):
    lexer = crear_lexer()
    lexer = crear_lexer()
    result = parser.parse(code, lexer=lexer)
    return result

# Ejemplo de uso
codigo_java = """
int x;
int suma(int a, int b) {
    x = a + b;
}
"""

ast = parse_code(codigo_java)

if ast:
    print_ast(ast)
    symbol_table.print_table()
else:
    print("Error de análisis.")

