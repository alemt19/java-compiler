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