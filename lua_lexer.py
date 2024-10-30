import ply.lex as lex

reserved = {'function': 'FUNCTION',
            'end': 'END',
            'local': 'LOCAL',
            'new': 'NEW'
            }

tokens = ['ID',
          'ASSIGN',
          'NUMBER',
          'STRING',
          'LPAREN',
          'RPAREN',
          'LCURLY',
          'RCURLY',
          'COMMA',
          'COLON',
          'DOT'
          ] + list(reserved.values())

t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r','
t_COLON = r':'
t_DOT = r'\.'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\".*?"'
    t.value = t.value[1:-1]
    return t


t_ignore = ' \t\n'


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()

data = '''
local a = 10
b = 321
local arr1 = {1, 2, 3}
arr2 = {4, 5, 6}
class = {}
MyClass = {property = 0}
'''

lexer.input(data)

if __name__ == '__main__':
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok.type, tok.value, tok.lexpos)
