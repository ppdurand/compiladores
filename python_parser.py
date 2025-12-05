import ply.yacc as yacc
from python_lexer import lexer, tokens


class ASTNode:
    """Nó da Árvore de Sintaxe Abstrata (AST)"""
    def __init__(self, type, children=None, value=None, lineno=None):
        self.type = type
        self.children = children if children is not None else []
        self.value = value
        self.lineno = lineno
    
    def __repr__(self):
        if self.value is not None:
            return f"{self.type}({self.value})"
        elif self.children:
            return f"{self.type}({len(self.children)} filhos)"
        else:
            return f"{self.type}"
    
    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.type}"
        
        if self.value is not None:
            result += f": {self.value}"
        
        if self.lineno is not None:
            result += f" [linha {self.lineno}]"
        
        result += "\n"
        
        for child in self.children:
            if isinstance(child, ASTNode):
                result += child.__str__(level + 1)
            else:
                result += f"{indent}  {child}\n"
        
        return result

precedence = (
    ('right', 'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'MOD_ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NOT_EQUAL'),
    ('left', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT', 'INCREMENT', 'DECREMENT'),
    ('left', 'LBRACKET'),
)

def p_program(p):
    '''program : statement_list'''
    p[0] = ASTNode('Program', [p[1]], lineno=p.lineno(1))

def p_statement_list(p):
    '''statement_list : statement_list statement
                     | statement
                     | empty'''
    if len(p) == 3:
        p[0] = ASTNode('StatementList', [p[1], p[2]], lineno=p.lineno(1))
    elif len(p) == 2 and p[1] is not None:
        p[0] = ASTNode('StatementList', [p[1]], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('StatementList', [], lineno=p.lineno(1))

def p_statement(p):
    '''statement : declaration
                 | expression_statement
                 | if_statement
                 | while_statement
                 | for_statement
                 | return_statement
                 | break_statement
                 | continue_statement
                 | block'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON
                            | SEMICOLON'''
    if len(p) == 3:
        p[0] = ASTNode('ExpressionStatement', [p[1]], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('ExpressionStatement', [], lineno=p.lineno(1))

def p_block(p):
    '''block : LBRACE statement_list RBRACE'''
    p[0] = ASTNode('Block', [p[2]], lineno=p.lineno(1))

def p_declaration(p):
    '''declaration : type ID SEMICOLON
                   | type ID ASSIGN expression SEMICOLON
                   | type ID LBRACKET INT_LITERAL RBRACKET SEMICOLON'''
    if len(p) == 4:
        p[0] = ASTNode('Declaration', [
            ASTNode('Type', value=p[1], lineno=p.lineno(1)),
            ASTNode('ID', value=p[2], lineno=p.lineno(2))
        ], lineno=p.lineno(1))
    elif len(p) == 6:
        p[0] = ASTNode('Declaration', [
            ASTNode('Type', value=p[1], lineno=p.lineno(1)),
            ASTNode('ID', value=p[2], lineno=p.lineno(2)),
            p[4]
        ], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('ArrayDeclaration', [
            ASTNode('Type', value=p[1], lineno=p.lineno(1)),
            ASTNode('ID', value=p[2], lineno=p.lineno(2)),
            ASTNode('Size', value=p[4], lineno=p.lineno(4))
        ], lineno=p.lineno(1))

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR
            | VOID'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ASTNode('IfStatement', [p[3], p[5]], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('IfStatement', [p[3], p[5], p[7]], lineno=p.lineno(1))

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    p[0] = ASTNode('WhileStatement', [p[3], p[5]], lineno=p.lineno(1))

def p_for_statement(p):
    '''for_statement : FOR LPAREN for_init SEMICOLON for_cond SEMICOLON for_update RPAREN statement'''
    p[0] = ASTNode('ForStatement', [p[3], p[5], p[7], p[9]], lineno=p.lineno(1))

def p_for_init(p):
    '''for_init : type ID
                | type ID ASSIGN expression
                | expression
                | empty'''
    if len(p) == 3 and p[1] in ('int', 'float', 'char', 'void'):
        p[0] = ASTNode('Declaration', [
            ASTNode('Type', value=p[1], lineno=p.lineno(1)),
            ASTNode('ID', value=p[2], lineno=p.lineno(2))
        ], lineno=p.lineno(1))
    elif len(p) == 5 and p[1] in ('int', 'float', 'char', 'void'):
        p[0] = ASTNode('Declaration', [
            ASTNode('Type', value=p[1], lineno=p.lineno(1)),
            ASTNode('ID', value=p[2], lineno=p.lineno(2)),
            p[4]
        ], lineno=p.lineno(1))
    elif len(p) == 2:
        if p[1] is None:
            p[0] = ASTNode('Empty', [], lineno=p.lineno(1))
        else:
            p[0] = p[1]

def p_for_cond(p):
    '''for_cond : expression
                | empty'''
    p[0] = p[1] if p[1] is not None else ASTNode('Empty', [], lineno=p.lineno(1))

def p_for_update(p):
    '''for_update : expression
                  | empty'''
    p[0] = p[1] if p[1] is not None else ASTNode('Empty', lineno=p.lineno(1))

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    if len(p) == 4:
        p[0] = ASTNode('ReturnStatement', [p[2]], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('ReturnStatement', [], lineno=p.lineno(1))

def p_break_statement(p):
    '''break_statement : BREAK SEMICOLON'''
    p[0] = ASTNode('BreakStatement', [], lineno=p.lineno(1))

def p_continue_statement(p):
    '''continue_statement : CONTINUE SEMICOLON'''
    p[0] = ASTNode('ContinueStatement', [], lineno=p.lineno(1))

def p_expression_assign(p):
    '''expression : ID ASSIGN expression
                  | ID PLUS_ASSIGN expression
                  | ID MINUS_ASSIGN expression
                  | ID TIMES_ASSIGN expression
                  | ID DIVIDE_ASSIGN expression
                  | ID MOD_ASSIGN expression
                  | array_access ASSIGN expression'''
    if isinstance(p[1], ASTNode) and p[1].type == 'ArrayAccess':
        p[0] = ASTNode('ArrayAssignment', [
            p[1],
            ASTNode('Operator', value=p[2], lineno=p.lineno(2)),
            p[3]
        ], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('Assignment', [
            ASTNode('ID', value=p[1], lineno=p.lineno(1)),
            ASTNode('Operator', value=p[2], lineno=p.lineno(2)),
            p[3]
        ], lineno=p.lineno(1))

def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression LESS expression
                  | expression LESS_EQUAL expression
                  | expression GREATER expression
                  | expression GREATER_EQUAL expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ASTNode('BinaryOp', [
        p[1],
        p[3]
    ], value=p[2], lineno=p.lineno(2))

def p_expression_unary(p):
    '''expression : NOT expression
                  | MINUS expression
                  | INCREMENT ID
                  | DECREMENT ID
                  | ID INCREMENT
                  | ID DECREMENT'''
    if p[1] in ('++', '--'):
        p[0] = ASTNode('UnaryOp', [
            ASTNode('ID', value=p[2], lineno=p.lineno(2))
        ], value=p[1], lineno=p.lineno(1))
    elif len(p) == 3 and isinstance(p[2], str) and p[2] in ('++', '--'):
        p[0] = ASTNode('UnaryOp', [
            ASTNode('ID', value=p[1], lineno=p.lineno(1))
        ], value=p[2], lineno=p.lineno(2))
    else:
        p[0] = ASTNode('UnaryOp', [p[2]], value=p[1], lineno=p.lineno(1))

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_array_access(p):
    '''array_access : ID LBRACKET expression RBRACKET'''
    p[0] = ASTNode('ArrayAccess', [
        ASTNode('ID', value=p[1], lineno=p.lineno(1)),
        p[3]
    ], lineno=p.lineno(1))

def p_expression_array_access(p):
    '''expression : array_access'''
    p[0] = p[1]

def p_expression_function_call(p):
    '''expression : ID LPAREN argument_list RPAREN
                  | ID LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ASTNode('FunctionCall', [
            ASTNode('ID', value=p[1], lineno=p.lineno(1)),
            p[3]
        ], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('FunctionCall', [
            ASTNode('ID', value=p[1], lineno=p.lineno(1)),
            ASTNode('ArgumentList', [], lineno=p.lineno(1))
        ], lineno=p.lineno(1))

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = ASTNode('ArgumentList', p[1].children + [p[3]], lineno=p.lineno(1))
    else:
        p[0] = ASTNode('ArgumentList', [p[1]], lineno=p.lineno(1))

def p_expression_literal(p):
    '''expression : INT_LITERAL
                  | FLOAT_LITERAL
                  | CHAR_LITERAL
                  | STRING_LITERAL'''
    p[0] = ASTNode('Literal', value=p[1], lineno=p.lineno(1))

def p_expression_id(p):
    '''expression : ID'''
    p[0] = ASTNode('ID', value=p[1], lineno=p.lineno(1))

def p_empty(p):
    '''empty :'''
    p[0] = None

def p_error(p):
    if p:
        print(f"❌ Erro sintático na linha {p.lineno}: token inesperado '{p.value}' (tipo: {p.type})")
        print(f"   Contexto: ...{p.value}...")
    else:
        print("❌ Erro sintático: fim inesperado do arquivo")

parser = yacc.yacc(debug=False, write_tables=False)

def parse_code(code):
    try:
        ast = parser.parse(code, lexer=lexer, tracking=True)
        return ast
    except Exception as e:
        print(f"❌ Erro ao analisar código: {e}")
        return None

