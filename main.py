from colorama import Fore, init
from calculations import evaluate_expression
from games import game_mode

init(autoreset=True)

HELP_MESSAGE = (
    '\n· <expression> — just type a mathematical expression to calculate it\n'
    '· help — show this list\n'
    '· quit, exit — exit the program\n'
    '· games — select a mini-game from the list\n')


def process_command(command):
    command = command.strip().lower()

    if not command:
        return True

    if command in ('quit', 'exit'):
        print('Goodbye!')
        return False

    elif command == 'help':
        print(HELP_MESSAGE)

    elif command == 'games':
        game_mode()

    elif not command[0].isalpha():
        try:
            print(evaluate_expression(command))
        except Exception as e:
            print(f'Calculation error: {e}')

    else:
        print(f"Unknown command '{command}'.")

    return True


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
