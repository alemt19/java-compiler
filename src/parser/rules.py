from ast_nodes import *
from sym_table import symbol_table


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
)

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
    else:
        print("Error de sintaxis: fin de archivo inesperado")