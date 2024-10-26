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


def p_expression_local_identifier(p):
    """expression : LOCAL ID ASSIGN NUMBER
                  | ID ASSIGN NUMBER"""
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
                       | ID
                       | NUMBER"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}, {p[3]}"


def p_expression_class(p):
    """expression : ID ASSIGN LCURLY RCURLY"""
    p[0] = f"{p[1]} = {{}}"


def p_expression_function(p):
    """expression : FUNCTION ID LPAREN RPAREN END"""
    p[0] = f"function {p[2]}() end"


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
