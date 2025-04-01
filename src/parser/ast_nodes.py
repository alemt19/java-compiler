class Program:
    def __init__(self, declarations):
        self.declarations = declarations

    def accept(self, visitor):
        return visitor.visit_program(self)

class VariableDeclaration:
    def __init__(self, type, name, expression=""):
        self.type = type
        self.name = name
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_variable_declaration(self)

class FunctionDeclaration:
    def __init__(self, modifiers, return_type, name, params, body):
        self.modifiers = modifiers
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_declaration(self)

class ClassDeclaration:
    def __init__(self, name, members, modifier=""):
        self.modifier = modifier
        self.name = name
        self.members = members

    def accept(self, visitor):
        return visitor.visit_class_declaration(self)

class Parameter:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def accept(self, visitor):
        return visitor.visit_parameter(self)

class Block:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self)

class Assignment:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_assignment(self)

class BinaryOperation:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_operation(self)

class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def accept(self, visitor):
        return visitor.visit_if_statement(self)

class ForLoop:
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for_loop(self)

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_loop(self)

class Identifier:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_identifier(self)

class Literal:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

class ArrayType:
    def __init__(self, base_type):
        self.base_type = base_type

    def accept(self, visitor):
      return visitor.visit_array_type(self)

class Type:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_type(self)

class VoidType:
    def __init__(self):
        self.name = "void"

    def accept(self, visitor):
        return visitor.visit_void_type(self)

def get_ast_str(node, prefix="", is_last=True):
    """
    Construye y retorna un string que representa el AST de forma jerárquica con líneas y nodos.

    Args:
        node (object): Nodo AST a procesar.
        prefix (str): Prefijo para la línea actual.
        is_last (bool): Indica si el nodo actual es el último hijo.

    Returns:
        str: String que representa el AST.
    """
    if node is None:
        return ""

    # Construir el prefijo y el nodo
    line_prefix = prefix + ("└── " if is_last else "├── ")
    node_str = line_prefix

    if isinstance(node, Program):
        node_str += "Program\n"
        children = node.declarations
    elif isinstance(node, ClassDeclaration): # Agregado manejo de ClassDeclaration
        node_str += f"ClassDeclaration: {node.modifier} class {node.name}\n"
        children = node.members
    elif isinstance(node, VariableDeclaration):
        if node.expression and isinstance(node.expression, Literal): #agregado manejo de expression
            node_str += f"VariableDeclaration: {node.type.name} {node.name} = {node.expression.value}\n"
        elif node.expression and isinstance(node.expression, BinaryOperation): 
            node_str += f"VariableDeclaration: {node.type.name} {node.name} = {node.expression.left.value} {node.expression.operator} {node.expression.right.value}\n"
        else:
            node_str += f"VariableDeclaration: {node.type.name} {node.name}\n"
        children = []
    elif isinstance(node, FunctionDeclaration):
        node_str += f"FunctionDeclaration: {" ".join(node.modifiers)} {node.return_type.name} {node.name}\n"
        children = node.params + [node.body]
    elif isinstance(node, Parameter):
        if isinstance(node.type, ArrayType):
            node_str += f"Parameter: {node.type.base_type.name}[] {node.name}\n"
        elif isinstance(node.type, Type):
            node_str += f"Parameter: {node.type.name} {node.name}\n"
        children = []
    elif isinstance(node, Block):
        node_str += "Block\n"
        children = node.statements
    elif isinstance(node, Assignment):
        node_str += "Assignment\n"
        children = [node.left, node.right]
    elif isinstance(node, BinaryOperation):
        node_str += f"BinaryOperation: {node.operator}\n"
        children = [node.left, node.right]
    elif isinstance(node, IfStatement):
        node_str += "IfStatement\n"
        children = [node.condition, node.then_block]
        if node.else_block:
            children.append(node.else_block)
    elif isinstance(node, ForLoop):
        node_str += "ForLoop\n"
        children = [node.init, node.condition, node.increment, node.body]
    elif isinstance(node, WhileLoop):
        node_str += "WhileLoop\n"
        children = [node.condition, node.body]
    elif isinstance(node, Identifier):
        node_str += f"Identifier: {node.value}\n"
        children = []
    elif isinstance(node, Literal):
        node_str += f"Literal: {node.value}\n"
        children = []
    elif isinstance(node, ArrayType): #agregado ArrayType
      node_str += f"ArrayType: {node.base_type}[]\n"
      children = []
    else:
        node_str += f"Unknown Node: {node}\n"
        children = []

    child_count = len(children)
    for i, child in enumerate(children):
        is_child_last = i == child_count - 1
        new_prefix = prefix + ("    " if is_last else "│   ")
        node_str += get_ast_str(child, new_prefix, is_child_last)

    return node_str