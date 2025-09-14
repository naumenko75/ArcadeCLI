import operator
from colorama import Fore, init
init(autoreset=True)

OPERATORS = {'+': (1, operator.add), '-': (1, operator.sub),
             '*': (2, operator.mul), '/': (2, operator.truediv),
             '^': (3, operator.pow)}

HELP_MESSAGE = (
    '\n· <expression> — just type a mathematical expression to calculate it\n'
    '· help — show this list\n'
    '· quit, exit — exit the program\n')


def process_command(command):
    command = command.strip().lower()

    if not command:
        return True

    if command in ('quit', 'exit'):
        return False

    elif command == 'help':
        print(HELP_MESSAGE)

    else:
        try:
            print(calculate(command))
        except Exception as e:
            print(f'Calculation error: {e}')

    return True


def calculate(formula):
    def parse(formula_string):
        number = ''
        for s in formula_string:
            if s in '1234567890.':
                number += s
            elif number:
                yield float(number)
                number = ''
            if s in OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

    def shunting_yard(parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
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

    def evaluate(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                stack.append(OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0]

    return evaluate(shunting_yard(parse(formula)))


def main():
    print(Fore.LIGHTWHITE_EX + 'Welcome to ArcadeCLI — console program made for fun.'
          '\nType "help" to see the commands.')

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
