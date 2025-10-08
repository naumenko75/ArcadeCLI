from colorama import Fore, init
from games import game_mode, start_game_by_input
from divisors import divisors_mode

init(autoreset=True)

HELP_MESSAGE = (
    "\n· help — show this list\n"
    "· quit — exit the program\n"
    "· games — enter game selection mode\n"
    "· game [name/number] — quick launch a specific game\n"
    "· divisors [number] — show the number of divisors for a given number\n"
    "· divisors [start] [end] — find the number with the most divisors in a range\n")


def process_command(command):
    """
    Processes the command and its arguments entered by the user.
    :param command: the string with a command
    :return: True (continue program) or False (exit program)
    """
    command = command.strip()

    if not command:
        return True

    parts = command.split()
    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in ('quit', 'exit'):
        print("Goodbye!")
        return False

    elif cmd in ('help', '?'):
        print(HELP_MESSAGE)

    elif cmd == 'games':
        game_mode()

    elif cmd == 'game':
        # Quick launch specific game
        if not args:
            print(f"{Fore.YELLOW}Usage: game [game_number] or game [game_name]{Fore.RESET}")
            print(f"Type {Fore.CYAN}games{Fore.RESET} to see available games")
        else:
            start_game_by_input(" ".join(args))

    elif cmd == 'divisors':
        divisors_mode(args)

    else:
        print(f"Unknown command '{command}'.")

    return True


def main():
    print("Welcome to ArcadeCLI — console program made for fun.")
    print("Type 'help' for more information.")

    while True:
        try:
            user_input = input(Fore.GREEN + '>>> ' + Fore.RESET)
            if not process_command(user_input):
                break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
