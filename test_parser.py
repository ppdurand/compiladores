import os
from python_parser import parse_code

def test_file(filename):
    print("=" * 60)
    print(f"Testando: {filename}")
    print("=" * 60)
    
    filepath = os.path.join('exemplos', filename)
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return
    
    with open(filepath, 'r') as f:
        code = f.read()
    
    print("\nCódigo:")
    print(code)
    print("\n" + "-" * 60)
    
    ast = parse_code(code)
    if ast:
        print("\nAST gerada:")
        print(ast)
    print("\n")

if __name__ == "__main__":
    test_files = [
        'exemplo1_declaracoes.c',
        'exemplo2_controle.c',
        'exemplo3_expressoes.c',
        'exemplo4_arrays.c',
        'exemplo5_erro_sintatico.c',
        'exemplo6_erro_lexico.c',
        'exemplo7_valido.c',
        'exemplo8_valido.c',
        'exemplo9_valido.c',
        'exemplo10_erro.c'
    ]
    
    for filename in test_files:
        test_file(filename)
        print()

