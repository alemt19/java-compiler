import ply.yacc as yacc

def p_declaracion_variable(p):
    '''declaracion : tipo ID PUNTOCOMA'''
    # Aquí puedes procesar la declaración de variable
    print(f"Declaración de variable: {p[1]} {p[2]}")

def p_declaracion_funcion(p):
    '''declaracion : tipo ID LPAREN lista_parametros RPAREN bloque'''
    # Aquí puedes procesar la declaración de función
    print(f"Declaración de función: {p[1]} {p[2]}")

def p_lista_parametros(p):
    '''lista_parametros : lista_parametros COMA tipo ID
                       | tipo ID
                       |'''
    # Aquí puedes procesar los parámetros de la función
    if len(p) > 1:
        print(f"Parámetro: {p[1]} {p[2]}")

def p_bloque(p):
    '''bloque : LLLAVE lista_sentencias RLLAVE'''
    # Aquí puedes procesar el bloque de código dentro de la función
    pass

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | sentencia
                        |'''
    # Aquí puedes procesar las sentencias dentro del bloque
    if len(p) > 1:
        pass

def p_expresion_aritmetica(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIV expresion'''
    # Aquí puedes procesar la expresión aritmética
    print(f"Operación aritmética: {p[1]} {p[2]} {p[3]}")

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    # Aquí puedes procesar la expresión lógica
    print(f"Operación lógica: {p[1]} {p[2]} {p[3]}")

def p_asignacion(p):
    '''sentencia : ID IGUAL expresion PUNTOCOMA'''
    # Aquí puedes procesar la asignación
    print(f"Asignación: {p[1]} = {p[3]}")

# Condicionales
def p_sentencia_if(p):
    '''sentencia : IF LPAREN expresion RPAREN bloque
                 | IF LPAREN expresion RPAREN bloque ELSE bloque'''
    # Aquí puedes procesar el condicional if
    print(f"Condicional if: {p[3]}")

def p_sentencia_else_if(p):
    '''sentencia : IF LPAREN expresion RPAREN bloque ELSE IF LPAREN expresion RPAREN bloque'''
    # Aquí puedes procesar el condicional else if
    print(f"Condicional else if: {p[3]} {p[9]}")

# Ciclos
def p_sentencia_for(p):
    '''sentencia : FOR LPAREN tipo ID IGUAL expresion PUNTOCOMA expresion PUNTOCOMA expresion RPAREN bloque'''
    # Aquí puedes procesar el ciclo for
    print(f"Ciclo for: {p[4]} = {p[6]}")

def p_sentencia_while(p):
    '''sentencia : WHILE LPAREN expresion RPAREN bloque'''
    # Aquí puedes procesar el ciclo while
    print(f"Ciclo while: {p[3]}")


# Manejo de errores
def p_error(p):
    if p:
        print(f"Error de sintaxis en la entrada: {p.value}")
    else:
        print("Error de sintaxis: fin de archivo inesperado")


precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV'),
)

parser = yacc.yacc()
