from .ast_nodes import VoidType

class CodeGeneratorVisitor:
    def __init__(self):
        self.current_class = None
        self.indent_level = 0

    def _indent(self, code):
        return '\n'.join(['    ' * self.indent_level + line for line in code.split('\n')])

    def visit_program(self, node):
        return '\n\n'.join([decl.accept(self) for decl in node.declarations])

    def visit_class_declaration(self, node):
        self.current_class = node.name
        class_code = f"class {node.name}:\n"
        self.indent_level += 1

        members_code = []
        for member in node.members:
            code = member.accept(self)
            members_code.append(self._indent(code) if code else '    pass')

        self.indent_level -= 1
        self.current_class = None
        return class_code + '\n\n'.join(members_code).strip() or '    pass'

    def visit_function_declaration(self, node):
        params = ', '.join([param.accept(self) for param in node.params])
        return_type = '' if isinstance(node.return_type, VoidType) else ''

        self.indent_level += 1
        body_code = node.body.accept(self)
        self.indent_level -= 1

        return f"def {node.name}({params}):\n{self._indent(body_code)}"

    def visit_variable_declaration(self, node):
        if node.expression:
            expr_code = node.expression.accept(self)
            return f"{node.name} = {expr_code}"
        else:
            return f"{node.name.value} = None  # Tipo original: {node.type.name}"

    def visit_parameter(self, node):
        return node.name  # Python no requiere tipos en parámetros

    def visit_block(self, node):
        statements = [stmt.accept(self) for stmt in node.statements]
        return '\n'.join(statements)

    def visit_assignment(self, node):
        return f"{node.left.accept(self)} = {node.right.accept(self)}"

    def visit_binary_operation(self, node):
        return f"{node.left.accept(self)} {node.operator} {node.right.accept(self)}"

    def visit_if_statement(self, node):
        condition = node.condition.accept(self)
        then_code = node.then_block.accept(self)

        result = [f"if {condition}:\n{self._indent(then_code)}"]

        if node.else_block:
            else_code = node.else_block.accept(self)
            result.append(f"else:\n{self._indent(else_code)}")

        return '\n'.join(result)

    def visit_for_loop(self, node):
        init = node.init.accept(self)
        condition = node.condition.accept(self)
        increment = node.increment.accept(self)

        if ' < ' in condition and '++' in increment:
            var = node.init.name.value
            end_value = condition.split(' < ')[1]
            return f"for {var} in range({init.split(' = ')[1]}, {end_value}):\n{self._indent(node.body.accept(self))}"

        return (
            f"{init}\n"
            f"while {condition}:\n"
            f"{self._indent(node.body.accept(self))}\n"
            f"{self._indent(increment)}"
        )

    def visit_while_loop(self, node):
        condition = node.condition.accept(self)
        body = node.body.accept(self)
        return f"while {condition}:\n{self._indent(body)}"

    def visit_identifier(self, node):
        return node.value

    def visit_literal(self, node):
        if isinstance(node.value, str):
            return f'"{node.value}"'
        return str(node.value)

    def visit_type(self, node):
        return ''  # Python no necesita declaraciones de tipo

    def visit_void_type(self, node):
        return ''

    def visit_array_type(self, node):
        return '' #python no define tipos de Array, por lo que no hace nada.