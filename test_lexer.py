from python_lexer import lexer

def test_lexer(code):
    print("Código:")
    print(code)
    print("\nTokens:")
    lexer.input(code)
    for tok in lexer:
        print(tok)
    print()

if __name__ == "__main__":
    code = '''
    int x = 10;
    float y = 3.14;
    char c = 'a';
    
    if (x >= 10) {
        y += x;
    }
    '''
    test_lexer(code)

