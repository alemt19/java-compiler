import ply.yacc as yacc
from os import path
import sys
from pathlib import Path

# Asegúrate de que el directorio del paquete esté en sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lexer.lexer import tokens, crear_lexer

# Precedencia

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
)

# Nodos AST

class Program:
    def __init__(self, declarations):
        self.declarations = declarations

class VariableDeclaration:
    def __init__(self, type, name):
        self.type = type
        self.name = name

class FunctionDeclaration:
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

class Parameter:
    def __init__(self, type, name):
        self.type = type
        self.name = name

class Block:
    def __init__(self, statements):
        self.statements = statements

class Assignment:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class BinaryOperation:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ForLoop:
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Identifier:
    def __init__(self, name):
        self.name = name

class Literal:
    def __init__(self, value):
        self.value = value

def print_ast(node, indent=0):
    """
    Imprime el AST de forma jerárquica.

    Args:
        node (object): Nodo AST a imprimir.
        indent (int): Nivel de indentación.
    """
    if isinstance(node, Program):
        print(f"{'  ' * indent}Program:")
        for declaration in node.declarations:
            print_ast(declaration, indent + 1)
    elif isinstance(node, VariableDeclaration):
        print(f"{'  ' * indent}VariableDeclaration: {node.type} {node.name}")
    elif isinstance(node, FunctionDeclaration):
        print(f"{'  ' * indent}FunctionDeclaration: {node.return_type} {node.name}")
        print(f"{'  ' * (indent + 1)}Parameters:")
        for param in node.params:
            print_ast(param, indent + 2)
        print(f"{'  ' * (indent + 1)}Body:")
        print_ast(node.body, indent + 2)
    elif isinstance(node, Parameter):
        print(f"{'  ' * indent}Parameter: {node.type} {node.name}")
    elif isinstance(node, Block):
        print(f"{'  ' * indent}Block:")
        for statement in node.statements:
            print_ast(statement, indent + 1)
    elif isinstance(node, Assignment):
        print(f"{'  ' * indent}Assignment:")
        print_ast(node.left, indent + 1)
        print(f"{'  ' * (indent + 1)}=")
        print_ast(node.right, indent + 1)
    elif isinstance(node, BinaryOperation):
        print(f"{'  ' * indent}BinaryOperation: {node.operator}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, IfStatement):
        print(f"{'  ' * indent}IfStatement:")
        print(f"{'  ' * (indent + 1)}Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{'  ' * (indent + 1)}Then:")
        print_ast(node.then_block, indent + 2)
        if node.else_block:
            print(f"{'  ' * (indent + 1)}Else:")
            print_ast(node.else_block, indent + 2)
    elif isinstance(node, ForLoop):
        print(f"{'  ' * indent}ForLoop:")
        print(f"{'  ' * (indent + 1)}Init:")
        print_ast(node.init, indent + 2)
        print(f"{'  ' * (indent + 1)}Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{'  ' * (indent + 1)}Increment:")
        print_ast(node.increment, indent + 2)
        print(f"{'  ' * (indent + 1)}Body:")
        print_ast(node.body, indent + 2)
    elif isinstance(node, WhileLoop):
        print(f"{'  ' * indent}WhileLoop:")
        print(f"{'  ' * (indent + 1)}Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{'  ' * (indent + 1)}Body:")
        print_ast(node.body, indent + 2)
    elif isinstance(node, Identifier):
        print(f"{'  ' * indent}Identifier: {node.name}")
    elif isinstance(node, Literal):
        print(f"{'  ' * indent}Literal: {node.value}")
    else:
        print(f"{'  ' * indent}Unknown Node: {node}")

# Tabla de símbolos mejorada

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]

    def insert(self, name, type, kind, value=None, params=None):
        self.scopes[-1][name] = {
            'type': type,
            'kind': kind,
            'value': value,
            'params': params
        }

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def update_value(self, name, value):
        symbol = self.lookup(name)
        if symbol:
            symbol['value'] = value
        else:
            print(f"Error semántico: Variable '{name}' no declarada.")

    def print_table(self):
        print("Tabla de Símbolos:")
        for i, scope in enumerate(self.scopes):
            print(f"  Ámbito {i}:")
            for name, info in scope.items():
                print(f"    {name}: {info}")

symbol_table = SymbolTable()

# Reglas gramaticales

def p_program(p):
    '''program : lista_declaraciones'''
    p[0] = Program(p[1])

def p_lista_declaraciones(p):
    '''lista_declaraciones : lista_declaraciones declaracion
                           | declaracion'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaracion(p):
    '''declaracion : declaracion_variable
                   | declaracion_funcion'''
    p[0] = p[1]

def p_tipo(p):
    '''tipo : INT_TYPE
            | FLOAT
            | BOOLEAN
            | CHAR
            | STRING'''
    p[0] = p[1]

def p_declaracion_variable(p):
    '''declaracion_variable : tipo IDENTIFIER SEMICOLON'''
    p[0] = VariableDeclaration(p[1], p[2])
    symbol_table.insert(p[2], p[1], 'variable')

def p_declaracion_funcion(p):
    '''declaracion_funcion : tipo IDENTIFIER LPAREN lista_parametros RPAREN bloque''' #Se modifico aqui
    p[0] = FunctionDeclaration(p[1], p[2], p[4], p[6])
    symbol_table.insert(p[2], p[1], 'function', params=p[4])

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros COMMA tipo IDENTIFIER
                       | tipo IDENTIFIER
                       |'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 3:
        p[0] = [Parameter(p[1], p[2])]
    else:
        p[0] = p[1] + [Parameter(p[3], p[4])]

def p_bloque(p):
    '''bloque : LBRACE lista_sentencias RBRACE'''
    p[0] = Block(p[2])

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | sentencia
                        |'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_expresion_aritmetica(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion MULT expresion
                 | expresion DIV expresion'''
    p[0] = BinaryOperation(p[2], p[1], p[3])

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = BinaryOperation(p[2], p[1], p[3])

def p_asignacion(p):
    '''sentencia : IDENTIFIER EQUALS expresion SEMICOLON'''
    p[0] = Assignment(Identifier(p[1]), p[3])
    symbol_table.update_value(p[1], p[3])

def p_sentencia_if(p):
    '''sentencia : IF LPAREN expresion RPAREN bloque
                 | IF LPAREN expresion RPAREN bloque ELSE bloque'''
    if len(p) == 6:
        p[0] = IfStatement(p[3], p[5])
    else:
        p[0] = IfStatement(p[3], p[5], p[7])

def p_sentencia_for(p):
    '''sentencia : FOR LPAREN tipo IDENTIFIER EQUALS expresion SEMICOLON expresion SEMICOLON expresion RPAREN bloque'''
    init = Assignment(Identifier(p[4]), p[6])
    condition = p[8]
    increment = p[10]
    p[0] = ForLoop(init, condition, increment, p[12])

def p_sentencia_while(p):
    '''sentencia : WHILE LPAREN expresion RPAREN bloque'''
    p[0] = WhileLoop(p[3], p[5])

def p_expresion_identificador(p):
    '''expresion : IDENTIFIER'''
    p[0] = Identifier(p[1])

def p_expresion_literal(p):
    '''expresion : NUMBER
                 | STRING_LITERAL
                 | CHARACTER_LITERAL
                 | BOOLEAN_LITERAL
                 | NULL_LITERAL'''
    p[0] = Literal(p[1])

# Manejo de errores

def p_error(p):
    if p:
        print(f"Error de sintaxis en la entrada: {p.value}")
        print(f"Token: {p}")  # Agrega este print para ver el token completo
    else:
        print("Error de sintaxis: fin de archivo inesperado")

parser = yacc.yacc()

def parse_code(code):
    lexer = crear_lexer()
    lexer.input(code)
    for tok in lexer:
        print(tok)  # Imprime cada token generado
    lexer = crear_lexer() #Reconstruimos el lexer
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

