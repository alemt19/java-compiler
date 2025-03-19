from .ast_nodes import *
from .sym_table import symbol_table
        
precedence = (
    ('left', 'COMMA'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'LTE', 'GT', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'ELSE')
)

def p_program(p):
    '''program : lista_declaraciones'''
    p[0] = Program(p[1])

def p_lista_declaraciones(p):
    '''lista_declaraciones : declaracion lista_declaraciones
                           | declaracion'''
    # print("p_lista_declaraciones:", p[:]) # Print de debug
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_declaracion(p):
    '''declaracion : declaracion_variable
                   | declaracion_funcion
                   | declaracion_clase'''
    # print("p_declaracion:", p[:]) # Print de debug
    p[0] = p[1]

def p_declaracion_clase(p):
    '''declaracion_clase : CLASS IDENTIFIER LBRACE lista_miembros RBRACE
                         | modificador CLASS IDENTIFIER LBRACE lista_miembros RBRACE'''

    # print("p_declaracion_clase:", p[:]) # Print de debug
    if len(p) == 7:
        p[0] = ClassDeclaration(p[3], p[5], p[1])
    elif len(p) == 6:
        p[0] = ClassDeclaration(p[2], p[4])
    
def p_lista_miembros(p):
    '''lista_miembros : lista_miembros miembro
                      | miembro
                      |''' # se agrega la produccion vacia
    # print("p_lista_miembros:", p[:]) # Print de debug
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_miembro(p):
    '''miembro : declaracion_variable
               | declaracion_funcion'''
    # print("p_miembro:", p[:]) # Print de debug
    p[0] = p[1]

def p_tipo(p):
    '''tipo : simple_type
            | simple_type LBRACKET RBRACKET'''
    # print("p_tipo:", p[:]) # Print de debug
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = ArrayType(p[1])
    
def p_simple_type(p):
    '''simple_type : INT_TYPE
                   | FLOAT
                   | BOOLEAN
                   | CHAR
                   | STRING
                   | IDENTIFIER'''
    p[0] = Type(p[1])

def p_tipo_funcion(p):
    '''tipo_funcion : INT_TYPE
                    | FLOAT
                    | BOOLEAN
                    | CHAR
                    | STRING
                    | VOID'''
    # print("p_tipo_funcion:", p[:]) # Print de debug
    if p[1] == 'void':
        p[0] = VoidType()
    else:
        p[0] = Type(p[1])

def p_declaracion_variable(p):
    '''declaracion_variable : tipo IDENTIFIER EQUALS expresion SEMICOLON
                            | tipo IDENTIFIER SEMICOLON'''
    # print("p_declaracion_variable:", p[:]) # Print de debug
    if len(p) == 6:  # Declaración con asignación
        p[0] = VariableDeclaration(p[1], p[2], p[4])
        symbol_table.insert(p[2], p[1].name, 'variable', value=p[4])
    else:  # Declaración sin asignación
        p[0] = VariableDeclaration(p[1], p[2])
        symbol_table.insert(p[2], p[1].name, 'variable')


def p_declaracion_funcion(p):
    '''declaracion_funcion : lista_modificadores tipo_funcion IDENTIFIER LPAREN lista_parametros RPAREN bloque'''
    # print("p_declaracion_funcion:", p[:]) # Print de debug
    p[0] = FunctionDeclaration(p[1], p[2], p[3], p[5], p[7])
    symbol_table.insert(p[3], p[2], 'function', params=p[5])

def p_lista_modificadores(p):
    '''lista_modificadores : lista_modificadores modificador
                           | modificador'''
    # print("p_lista_modificadores:", p[:]) # Print de debug
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_modificador(p):
    '''modificador : PUBLIC
                   | PRIVATE
                   | PROTECTED
                   | STATIC'''
    # print("p_modificador:", p[:]) # Print de debug
    p[0] = p[1]

def p_lista_parametros(p):
    '''lista_parametros : parametro
                       | lista_parametros COMMA parametro
                       |''' 
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parametro(p):
    '''parametro : tipo IDENTIFIER'''
    p[0] = Parameter(p[1], p[2])


def p_bloque(p):
    '''bloque : LBRACE lista_sentencias RBRACE'''
    # print("p_bloque:", p[:]) # Print de debug
    p[0] = Block(p[2])

def p_lista_sentencias(p):
    '''lista_sentencias : sentencia lista_sentencias
                        | sentencia
                        |'''
    # print("p_lista_sentencias:", p[:]) # Print de debug
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_expresion(p):
    '''expresion : expresion_aritmetica
                 | expresion_logica
                 | expresion_identificador
                 | expresion_literal
                 | expresion_comparacion'''
    p[0] = p[1]

def p_expresion_aritmetica(p):
    '''expresion_aritmetica : expresion PLUS expresion
                            | expresion MINUS expresion
                            | expresion MULT expresion
                            | expresion DIV expresion'''
    p[0] = BinaryOperation(p[2], p[1], p[3])

def p_expresion_logica(p):
    '''expresion_logica : expresion AND expresion
                        | expresion OR expresion'''
    p[0] = BinaryOperation(p[2], p[1], p[3])

def p_expresion_identificador(p):
    '''expresion_identificador : IDENTIFIER'''
    p[0] = Identifier(p[1])

def p_expresion_literal(p):
    '''expresion_literal : NUMBER
                         | STRING_LITERAL
                         | CHARACTER_LITERAL
                         | BOOLEAN_LITERAL
                         | NULL_LITERAL'''
    p[0] = Literal(p[1])

def p_expresion_comparacion(p):
    '''expresion_comparacion : expresion LT expresion
                             | expresion LTE expresion
                             | expresion GT expresion
                             | expresion GTE expresion
                             | expresion EQ expresion
                             | expresion NEQ expresion'''
    p[0] = BinaryOperation(p[2], p[1], p[3])

def p_sentencia_declaracion_variable(p):
    '''sentencia : declaracion_variable'''
    # print("p_sentencia_declaracion_variable:", p[:]) # Print de debug
    p[0] = p[1]

def p_asignacion(p):
    '''sentencia : IDENTIFIER EQUALS expresion SEMICOLON'''
    p[0] = Assignment(Identifier(p[1]), p[3])
    symbol_table.update_value(p[1], p[3])
    # print("p_asignacion:", p[:]) # Print de debug

def p_sentencia_if(p):
    '''sentencia : IF LPAREN expresion RPAREN bloque
                 | IF LPAREN expresion RPAREN bloque ELSE bloque'''
    # print("p_sentencia_if:", p[:]) # Print de debug
    if len(p) == 6:
        p[0] = IfStatement(p[3], p[5])
    else:
        p[0] = IfStatement(p[3], p[5], p[7])

def p_sentencia_for(p):
    '''sentencia : FOR LPAREN tipo IDENTIFIER EQUALS expresion SEMICOLON expresion SEMICOLON expresion RPAREN bloque'''
    # print("p_sentencia_for:", p[:]) # Print de debug
    init = Assignment(Identifier(p[4]), p[6])
    condition = p[8]
    increment = p[10]
    p[0] = ForLoop(init, condition, increment, p[12])

def p_sentencia_while(p):
    # print("p_sentencia_while:", p[:]) # Print de debug
    '''sentencia : WHILE LPAREN expresion RPAREN bloque'''
    p[0] = WhileLoop(p[3], p[5])
