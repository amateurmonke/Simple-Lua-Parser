import ply.lex as lex
import ply.yacc as yacc

# Define tokens regex using lexer
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
    return t


t_ignore = ' \t\n'


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()


# Parse input strings using yacc
def p_expression_identifier(p):
    """expression : ID
                  | LOCAL ID"""
    if p[1] == 'local':
        p[0] = f"local {p[2]}"
    else:
        p[0] = p[1]


def p_expression_identifier_assign(p):
    """expression : LOCAL ID ASSIGN NUMBER
                  | ID ASSIGN NUMBER
                  | LOCAL ID ASSIGN STRING
                  | ID ASSIGN STRING"""
    if p[1] == 'local':
        p[0] = f"local {p[2]} = {p[4]}"
    else:
        p[0] = f"{p[1]} = {p[3]}"


def p_expression_array(p):
    """expression : ID ASSIGN LCURLY expression_list RCURLY
                  | LOCAL ID ASSIGN LCURLY expression_list RCURLY"""
    if p[1] == 'local':
        p[0] = f"local {p[2]} = {{{p[5]}}}"
    else:
        p[0] = f"{p[1]} = {{{p[4]}}}"


def p_expression_list(p):
    """expression_list : expression_list COMMA ID
                       | expression_list COMMA NUMBER
                       | expression_list COMMA STRING
                       | ID
                       | NUMBER
                       | STRING"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"


def p_expression_class(p):
    """expression : ID ASSIGN LCURLY RCURLY
                  | ID ASSIGN LCURLY prop_list RCURLY"""
    if len(p) == 4:
        p[0] = f"{p[1]} = {{}}"
    else:
        p[0] = f"{p[1]} = {{{p[4]}}}"


def p_prop_list(p):
    """prop_list : prop_list COMMA ID ASSIGN NUMBER
                 | prop_list COMMA ID ASSIGN STRING
                 | ID ASSIGN NUMBER
                 | ID ASSIGN STRING"""
    if len(p) == 2:
        p[0] = f"{p[1]} = {p[2]}"
    else:
        p[0] = f"{p[1]}, {p[3]}"


def p_identifier_list(p):
    """identifier_list : identifier_list COMMA ID
                       | ID"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"


def p_expression_function(p):
    """expression : FUNCTION ID LPAREN RPAREN END
                  | FUNCTION ID LPAREN identifier_list RPAREN END"""
    if len(p) == 6:
        p[0] = f"function {p[2]}() end"
    else:
        p[0] = f"function {p[2]}({p[4]}) end"


def p_expression_obj(p):
    """expression : ID ASSIGN ID COLON NEW LPAREN RPAREN
                  | ID ASSIGN ID COLON NEW LPAREN expression_list RPAREN
                  | LOCAL ID ASSIGN ID COLON NEW LPAREN RPAREN
                  | LOCAL ID ASSIGN ID COLON NEW LPAREN expression_list RPAREN
                  """
    if p[1] == 'local':
        if len(p) == 8:
            p[0] = f"local {p[2]} = {p[4]}:new()"
        else:
            p[0] = f"local {p[2]} = {p[4]}:new({p[8]})"
    else:
        if len(p) == 7:
            p[0] = f"{p[1]} = {p[3]}:new()"
        else:
            p[0] = f"{p[1]} = {p[3]}:new({p[7]})"


error = False


def p_error(p):
    global error
    error = True
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")


parser = yacc.yacc()

while True:
    try:
        data = input("Enter lua expression: ")
    except EOFError:
        break

    if not data:
        continue

    result = parser.parse(data)

    if error:
        error = False
        continue
    else:
        print("Parsed succesfully")
