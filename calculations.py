def evaluate_expression(s):
    def tokenize(s):
        tokens = []
        i = 0
        n = len(s)
        while i < n:
            if s[i] in ' \t':
                i += 1
                continue
            if s[i] in '()+-*/':
                tokens.append(s[i])
                i += 1
            elif s[i].isdigit() or s[i] == '.':
                j = i
                has_dot = False
                while j < n:
                    if s[j].isdigit():
                        j += 1
                    elif s[j] == '.':
                        if has_dot:
                            raise ValueError("several decimal points in the number")
                        has_dot = True
                        j += 1
                    else:
                        break
                num_str = s[i:j]
                try:
                    if has_dot:
                        tokens.append(float(num_str))
                    else:
                        tokens.append(int(num_str))
                except ValueError:
                    raise ValueError(f"invalid number '{num_str}'")
                i = j
            else:
                raise ValueError(f"invalid character '{s[i]}'")
        return tokens

    def process_tokens(tokens):
        if not tokens:
            return []

        new_tokens = []
        n = len(tokens)

        # Обработка унарных операторов
        for i in range(n):
            token = tokens[i]
            if token in ['+', '-']:
                # Определяем, является ли оператор унарным
                if i == 0 or (isinstance(tokens[i - 1], str) and tokens[i - 1] in '(*/+-'):
                    # Обрабатываем последовательные унарные операторы
                    if new_tokens and new_tokens[-1] in ['u+', 'u-']:
                        prev_unary = new_tokens[-1]
                        if token == '+':
                            new_tokens[-1] = 'u+' if prev_unary == 'u+' else 'u-'
                        else:
                            new_tokens[-1] = 'u-' if prev_unary == 'u+' else 'u+'
                    else:
                        new_tokens.append('u+' if token == '+' else 'u-')
                else:
                    new_tokens.append(token)
            else:
                # Вставка неявного умножения
                if (new_tokens and (isinstance(token, (int, float)) or token == '(') and
                        (isinstance(new_tokens[-1], (int, float)) or (
                            isinstance(new_tokens[-1], str) and new_tokens[-1] == ')'))):
                    new_tokens.append('*')
                new_tokens.append(token)

        return new_tokens

    def precedence(op):
        if op in ['u+', 'u-']:
            return 4  # Наивысший приоритет
        if op in ['*', '/']:
            return 3
        if op in ['+', '-']:
            return 2
        return 0

    def apply_operator(operators, values):
        op = operators.pop()
        if op in ['u+', 'u-']:
            if len(values) < 1:
                raise ValueError("not enough operands for unary operator")
            a = values.pop()
            values.append(a if op == 'u+' else -a)
        else:
            if len(values) < 2:
                raise ValueError("not enough operands for binary operator")
            b = values.pop()
            a = values.pop()
            if op == '+':
                values.append(a + b)
            elif op == '-':
                values.append(a - b)
            elif op == '*':
                values.append(a * b)
            elif op == '/':
                if b == 0:
                    raise ValueError("division by zero")
                values.append(a / b)

    tokens = tokenize(s)
    tokens = process_tokens(tokens)
    values = []
    operators = []

    for token in tokens:
        if isinstance(token, (int, float)):
            values.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            if not operators or operators[-1] != '(':
                raise ValueError("unbalancde parentheses")
            operators.pop()
        else:
            while (operators and operators[-1] != '(' and
                    precedence(operators[-1]) >= precedence(token)):
                apply_operator(operators, values)
            operators.append(token)

    while operators:
        if operators[-1] == '(':
            raise ValueError("unbalancde parentheses")
        apply_operator(operators, values)

    return values[0] if values else 0
