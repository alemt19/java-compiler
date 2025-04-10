#from ..parser.ast_nodes import Program, ,
from parser.ast_nodes import Program, FunctionDeclaration, VariableDeclaration, Literal
from semantic.sym_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
    
    def analyze(self, ast):
        self._visit_node(ast)
        return {
            "is_valid": len(self.errors) == 0,
            "errors": self.errors
        }
    
    def _visit_node(self, node):
        if isinstance(node, Program):
            self._visit_program(node)
        elif isinstance(node, FunctionDeclaration):
            self._visit_function_decl(node)
        elif isinstance(node, VariableDeclaration):
            self._visit_variable_decl(node)
        # Agrega más nodos según tu AST
    
    def _visit_program(self, node):
        for element in node.declarations:
            self._visit_node(element)
    
    def _visit_function_decl(self, node):
        func_name = node.name
        if self.symbol_table.lookup_current_scope(func_name):
            self.errors.append(f"Función '{func_name}' ya declarada")
        else:
            self.symbol_table.add(func_name, 'function')
            self.symbol_table.enter_scope()
            for param in node.params:
                self._visit_node(param)
            for stmt in node.body.statements:
                self._visit_node(stmt)
            self.symbol_table.exit_scope()
    
    ## analyzer.py (Fragmento modificado)
    def _visit_variable_decl(self, node):
        var_name = node.name
        if self.symbol_table.lookup_current_scope(var_name):
            self.errors.append(f"Variable '{var_name}' ya declarada")
        else:
            # Extraer el valor del Literal (si existe)
            value = node.expression.value if node.expression else None
            if isinstance(value, Literal):
                value = value.value  # Obtener el valor primitivo (ej: 10, "Hola")
            
            self.symbol_table.add(var_name, {
                "type": node.type.name if hasattr(node.type, 'name') else str(node.type),
                "kind": "variable",
                "value": value  # Ahora es un número o string
            })

# analyzer.py (Nuevo método)
def get_symbol_table_report(self):
    report = []
    for scope_level, scope in enumerate(self.symbol_table.scopes):
        report.append(f"Ámbito {scope_level}:")
        for name, details in scope.items():
            report.append(f"  {name}: {details['type']} (valor: {details.get('value', 'N/A')})")
    return "\n".join(report)

def analyze_code(ast):
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "symbol_table": analyzer.get_symbol_table_report()  # Cadena, no diccionario
    }