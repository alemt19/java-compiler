class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
    
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        self.scopes.pop()
    
    def add(self, name, symbol_type):
        self.scopes[-1][name] = symbol_type
    
    def lookup_current_scope(self, name):
        return self.scopes[-1].get(name, None)