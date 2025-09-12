import operator

OPERATORS = {
    '+': (1, operator.add, 2, 'left'),
    '-': (1, operator.sub, 2, 'left'),
    '*': (2, operator.mul, 2, 'left'),
    '/': (2, operator.truediv, 2, 'left'),
    '^': (3, operator.pow, 2, 'right'),
    'u+': (4, operator.pos, 'right'),
    'u-': (4, operator.neg, 1, 'right')
}


def arithmetic_eval(formula):
    formula = formula.replace(' ', '')

    def parse(formula_string):
        number = ''
        prev_token = None
        for s in formula_string:
            if s in '1234567890.':
                number += s
            else:
                if number:
                    yield float(number)
                    prev_token = float(number)
                    number = ''
                if s in OPERATORS or s in "()":
                    if s in '+-':
                        if prev_token is None or prev_token in OPERATORS or prev_token == '(':
                            yield 'u+' if s == '+' else 'u-'
                        else:
                            yield s
                    else:
                        yield s
                    prev_token = s
        if number:
            yield float(number)

    def shunting_yard(parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while stack and stack[-1] != "(" and (
                    (OPERATORS[token][0] < OPERATORS[stack[-1]][0]) or
                    (OPERATORS[token][0] == OPERATORS[stack[-1]][0] and OPERATORS[token][3] == 'left')
                ):
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:
                arity = OPERATORS[token][2]
                if arity == 1:
                    x = stack.pop()
                    stack.append(OPERATORS[token][1](x))
                else:
                    y, x = stack.pop(), stack.pop()
                    stack.append(OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0] if stack else 0.0

    return calc(shunting_yard(parse(formula)))
