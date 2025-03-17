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


def print_ast(node, prefix="", is_last=True):
    """
    Imprime el AST de forma jerárquica con líneas y nodos.

    Args:
        node (object): Nodo AST a imprimir.
        prefix (str): Prefijo para la línea actual.
        is_last (bool): Indica si el nodo actual es el último hijo.
    """
    if node is None:
        return

    # Imprimir el prefijo y el nodo
    line_prefix = prefix + ("└── " if is_last else "├── ")
    print(line_prefix, end="")

    if isinstance(node, Program):
        print("Program")
        children = node.declarations
    elif isinstance(node, VariableDeclaration):
        print(f"VariableDeclaration: {node.type} {node.name}")
        children = []
    elif isinstance(node, FunctionDeclaration):
        print(f"FunctionDeclaration: {node.return_type} {node.name}")
        children = node.params + [node.body]
    elif isinstance(node, Parameter):
        print(f"Parameter: {node.type} {node.name}")
        children = []
    elif isinstance(node, Block):
        print("Block")
        children = node.statements
    elif isinstance(node, Assignment):
        print("Assignment")
        children = [node.left, node.right]
    elif isinstance(node, BinaryOperation):
        print(f"BinaryOperation: {node.operator}")
        children = [node.left, node.right]
    elif isinstance(node, IfStatement):
        print("IfStatement")
        children = [node.condition, node.then_block]
        if node.else_block:
            children.append(node.else_block)
    elif isinstance(node, ForLoop):
        print("ForLoop")
        children = [node.init, node.condition, node.increment, node.body]
    elif isinstance(node, WhileLoop):
        print("WhileLoop")
        children = [node.condition, node.body]
    elif isinstance(node, Identifier):
        print(f"Identifier: {node.name}")
        children = []
    elif isinstance(node, Literal):
        print(f"Literal: {node.value}")
        children = []
    else:
        print(f"Unknown Node: {node}")
        children = []

    # Imprimir los hijos
    child_count = len(children)
    for i, child in enumerate(children):
        is_child_last = i == child_count - 1
        new_prefix = prefix + ("    " if is_last else "│   ")
        print_ast(child, new_prefix, is_child_last)