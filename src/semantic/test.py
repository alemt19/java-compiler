from analyzer import analyze_code

code = """
int x = 10;
int x = 20;  // Variable duplicada
"""

result = analyze_code(code)
print(result)
# Salida:
# {
#   "is_valid": False,
#   "errors": ["Variable 'x' ya declarada"]
# }