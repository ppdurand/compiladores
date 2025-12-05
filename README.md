# Analisador Léxico e Sintático para Linguagem C

Trabalho de Construção de Compiladores - AP3

## Estrutura do Projeto

```
compiladores/
├── python_lexer.py          # Analisador léxico
├── python_parser.py         # Analisador sintático
├── test_lexer.py            # Testes do lexer
├── test_parser.py           # Testes do parser
├── requirements.txt         # Dependências Python
├── exemplos/                # Exemplos de código C
│   ├── exemplo1_declaracoes.c
│   ├── exemplo2_controle.c
│   ├── exemplo3_expressoes.c
│   ├── exemplo4_arrays.c
│   ├── exemplo5_erro_sintatico.c
│   ├── exemplo6_erro_lexico.c
│   ├── exemplo7_valido.c
│   ├── exemplo8_valido.c
│   ├── exemplo9_valido.c
│   └── exemplo10_erro.c
├── DOCUMENTACAO_PARSER.txt   # Documentação técnica do parser
├── RELATORIO_TECNICO.txt     # Relatório técnico completo
└── requisitos_trabalho.txt  # Requisitos do trabalho
```

## Instalação

1. Criar ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Testar o Lexer
```bash
python test_lexer.py
```

### Testar o Parser
```bash
python test_parser.py
```

### Usar programaticamente
```python
from python_parser import parse_code

code = """
int x = 10;
if (x > 5) {
    x = x + 1;
}
"""

ast = parse_code(code)
if ast:
    print(ast)
```

## Exemplos

Os exemplos estão na pasta `exemplos/`:
- `exemplo1_declaracoes.c` - Declarações e expressões simples
- `exemplo2_controle.c` - Estruturas de controle (if, while, for)
- `exemplo3_expressoes.c` - Expressões complexas
- `exemplo4_arrays.c` - Arrays e funções
- `exemplo5_erro_sintatico.c` - Código com erro sintático
- `exemplo6_erro_lexico.c` - Código com erro léxico
- `exemplo7_valido.c` - Código válido
- `exemplo8_valido.c` - Código válido
- `exemplo9_valido.c` - Código válido
- `exemplo10_erro.c` - Código com erro

## Documentação

- `DOCUMENTACAO_PARSER.txt` - Documentação detalhada do parser

