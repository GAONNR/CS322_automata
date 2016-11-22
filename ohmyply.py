import ply
import ply.lex as lex
import ply.yacc as yacc

class Symbol:
    def __init__(self, value):
        self.value = value
        self.classtype = 'Symbol'
    def __str__(self):
        return '(Symbol ' + self.value + ')'

class Concat:
    def __init__(self, v1, v2):
        self.value = (v1, v2)
        self.classtype = 'Concat'
    def __str__(self):
        return '(Concat ' + str(self.value[0]) + ' ' + str(self.value[1]) + ')'

class Star:
    def __init__(self, value):
        self.value = value
        self.classtype = 'Star'
    def __str__(self):
        return '(Star ' + str(self.value) + ')'

class Or:
    def __init__(self, v1, v2):
        self.value = (v1, v2)
        self.classtype = 'Or'
    def __str__(self):
        return '(Or ' + str(self.value[0]) + ' ' + str(self.value[1]) + ')'

class Epsilon:
    def __init__(self):
        self.value = 'E'
        self.classtype = 'Epsilon'
    def __str__(self):
        return 'E'

tokens = (
        'SYMBOL',
        'OR', 'STAR',
        'LPAREN', 'RPAREN'
        )

t_SYMBOL    = r'[a-zA-Z0-9]'
t_OR        = r'\+'
t_STAR      = r'\*'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

t_ignore    = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


# lex.input("ba*(a+b)")
# for tok in iter(lex.token, None):
#    print(repr(tok.type), repr(tok.value))

# print("-----------------------------")

symbols = set()

precedence = (
    ('left', 'CONCAT'),
    # ('left', 'PAREN'),
    ('left', 'STAR'),
    )

def p_expression_or(p):
    'expression : expression OR expression'
    # print("or:", p[1], p[3])
    p[0] = Or(p[1], p[3])

def p_expression_star(p):
    'expression : expression STAR'
    # print("star:", p[1])
    p[0] = Star(p[1])

def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
               | LPAREN RPAREN
    '''
    # print("paren")
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = Epsilon()


def p_expression_concat(p):
    'expression : expression expression %prec CONCAT'
    # print ("concat", p[1], p[2])
    p[0] = Concat(p[1], p[2])

def p_expression_symbol(p):
    'expression : SYMBOL'
    # print("symbol", p[1])
    symbols.add(p[1])
    p[0] = Symbol(p[1])

def p_error(p):
     print("Syntax error at '%s'" % p.value)

yacc.yacc()

def parse(string):
    return yacc.parse(string)

if __name__ == '__main__':
    ihaveainput = input("Give me a string: ")
    parsed = yacc.parse(ihaveainput)
    print(parsed)
