import ply.yacc as yacc
from lua_lexer import tokens


# def p_statement_expression(p):
#     """statement : expression"""
#     print(f"Accepted expression: {p[1]}")


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
    p[0] = f"{p[1]} = {{}}"


def p_prop_list(p):
    """prop_list : prop_list COMMA ID ASSIGN NUMBER
                 | prop_list COMMA ID ASSIGN STRING
                 | ID ASSIGN NUMBER
                 | ID ASSIGN STRING"""
    if len(p) == 2:
        p[0] = p[1]
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


def p_error(p):
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
    print(result)
