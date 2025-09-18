import random
from colorama import Fore, init

init(autoreset=True)

GAMES_LIST = (
    "\nYou're in game mode!"
    "\nEnter the minigame number to start 'q' to exit:\n"
    '1. Guess the number\n'
    '2. Rock paper scissors\n'
    '3. Hangman\n'
    '4. Tic-tac-toe\n')


def game_command_processing(command):
    command = command.strip().lower()

    if not command:
        return True

    if command in ('q', 'quit', 'exit'):
        print('You have exited game mode.\n')
        return False

    elif command == '1':
        guess_number()

    elif command == '2':
        rock_paper_scissors()

    else:
        print('Enter the game number.')

    return True


def guess_number():
    number = random.randint(1, 100)
    attempts = 0

    print("\nGuess the number from 1 to 100!")

    while True:
        try:
            user_input = input(Fore.GREEN + 'Your guess: ' +
                               Fore.RESET).strip().lower()

            if user_input.lower() in ('q', 'quit', 'exit'):
                print(f'Quitting the game. The hidden number was {number}.\n')
                break

            guess = int(user_input)
            attempts += 1

            if guess < number:
                print("More.")
            elif guess > number:
                print("Less.")
            else:
                print(f"Right! You guessed it in {attempts} tries.\n")
                break
        except ValueError:
            print("Enter an integer.")


def rock_paper_scissors():
    choices = ['rock', 'scissors', 'paper']

    while True:
        user_choice = input('\nChoose (rock, paper, or scissors): ').strip().lower()

        if user_choice == 'q':
            print('Quitting the game.\n')
            break

        if user_choice not in choices:
            print("Wrong choice.")
            continue

        comp_choice = random.choice(choices)
        print(f'The computer selected {comp_choice}.', end=' ')

        if user_choice == comp_choice:
            print('Draw!')
        elif (user_choice == 'rock' and comp_choice == 'scissors') or \
                (user_choice == 'scissors' and comp_choice == 'paper') or \
                (user_choice == 'paper' and comp_choice == 'rock'):
            print(Fore.LIGHTGREEN_EX + 'You won!' + Fore.RESET)
        else:
            print(Fore.LIGHTRED_EX + 'You lost!' + Fore.RESET)


def game_mode():
    print(GAMES_LIST)

    while True:
        try:
            user_input = input(Fore.GREEN + 'game> ' + Fore.RESET)
            if not game_command_processing(user_input):
                break
        except Exception as e:
            print(f'Unexpected error: {e}')
