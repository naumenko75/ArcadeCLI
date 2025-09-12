from arithmetic_parsing import arithmetic_eval
from colorama import Fore, init
init(autoreset=True)

help_message = ('<expression> — just type a mathematical expression to calculate it\n'
                'help — show this list\n'
                'quit, exit — exit the program')

def processing_commands():
    while True:
        command = input(Fore.GREEN + '>>> ' + Fore.RESET).strip()

        if command:
            if command in ('exit', 'quit'):
                print('Goodbye!', end='')
                break

            elif command == 'help':
                print(help_message)

            else:
                print(arithmetic_eval(''.join(command)))


def main():
    print('Welcome to ArcadeCLI — console program made for fun.\nType "help" to see the commands.')

    try:
        processing_commands()
    except Exception as e:
        print(f'Unexpected error: {e}')


if __name__ == '__main__':
    main()
