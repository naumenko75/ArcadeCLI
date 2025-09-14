from colorama import Fore, init
init(autoreset=True)

HELP_MESSAGE = (
    '\n· <expression> — just type a mathematical expression to calculate it\n'
    '· help — show this list\n'
    '· quit, exit — exit the program\n')


def process_command(command):
    command = command.strip().lower()

    # Обработка пустой команды
    if not command:
        return True

    # Обработка команды выхода
    if command in ('quit', 'exit'):
        return False

    # Обработка математического выражения
    elif command[0] in '01234567890.-+^/*':
        try:
            print(calculate(command))
        except Exception as e:
            print(f'Calculation error: {e}')

    # Обработка команды помощи
    elif command == 'help':
        print(HELP_MESSAGE)

    # Обработка неизвестной команды
    else:
        print(f'Unknown command: {command}')

    return True


def calculate(formula):
    # Функция парсинга
    def parse(s):
        s = s.replace(' ', '')
        tokens = []
        number = ''

        for i, char in enumerate(s):
            if char in '0123456789.':
                if char == '.':
                    if '.' in number:
                        raise SyntaxError(
                            'multiple decimal points used in number.')
                number += char

            elif not number and char in '+-':
                # Обработка унарных операторов
                tokens.append(char)

            elif char in '^*/+-':
                if not number:
                    raise SyntaxError('missing operand before operator.')

                # Добавляем число
                tokens.append(float(number) if '.' in number else int(number))
                # Добавляем оператор
                tokens.append(char)
                number = ''

            else:
                raise SyntaxError(f"extraneous character '{char}' used.")

        # Добавляем последнее число
        if not number:
            raise SyntaxError('expression ends with operator.')
        tokens.append(float(number) if '.' in number else int(number))

        return tokens

    # Функция вычисления
    def evaluate(tokens):
        # Функция для определения приоритета операторов
        def precedence(op):
            if op == '^':
                return 4
            elif op in '*/':
                return 3
            elif op in '+-':
                return 2
            return 0

        # Функция для применения оператора к операндам
        def apply_operator(operators, values):
            operator = operators.pop()
            right = values.pop()
            left = values.pop()

            if operator == '^':
                result = left ** right
            elif operator == '*':
                result = left * right
            elif operator == '/':
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                result = left / right
            elif operator == '+':
                result = left + right
            elif operator == '-':
                result = left - right

            values.append(result)

        # Конвертируем инфиксную запись в RPN и вычисляем
        operators = []
        values = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if isinstance(token, (int, float)):
                values.append(token)

            elif token in '^*/+-':
                # Обработка унарных операторов
                if (i == 0 or
                        (i > 0 and isinstance(tokens[i - 1], str) and
                         tokens[i - 1] in '^*/+-')):
                    # Это унарный оператор
                    if token == '-':
                        values.append(0)
                        operators.append('-')
                    elif token == '+':
                        # Унарный плюс можно игнорировать
                        pass
                    i += 1
                    continue

                # Для бинарных операторов
                while (operators and operators[-1] != '(' and
                       precedence(operators[-1]) >= precedence(token)):
                    apply_operator(operators, values)
                operators.append(token)

            i += 1

        # Применяем оставшиеся операторы
        while operators:
            apply_operator(operators, values)

        result = values[0]

        # Возвращаем int если результат целый, иначе float
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result

    return evaluate(parse(formula))


def main():
    print('Welcome to ArcadeCLI — console program made for fun.\nType "help" to see the commands.')

    while True:
        try:
            user_input = input(Fore.GREEN + '>>> ' + Fore.RESET)
            if not process_command(user_input):
                break
        except KeyboardInterrupt:
            print('\nTerminating the program.', end='')
            break
        except Exception as e:
            print(f'Unexpected error: {e}')


if __name__ == '__main__':
    main()
