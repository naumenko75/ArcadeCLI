import random
from colorama import Fore, init

init(autoreset=True)


def guess_number():
    """
    Guess the Number game logic.
    Player tries to guess a randomly generated number between 1 and 100.
    """
    number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print(f"\n{Fore.CYAN}Guess the Number Game")
    print(f"I'm thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts to guess it.{Fore.RESET}\n")

    while attempts < max_attempts:
        attempts += 1
        attempts_left = max_attempts - attempts + 1

        try:
            guess = input(f"{Fore.YELLOW}Attempt {attempts}/{max_attempts}. Enter your guess: {Fore.RESET}")

            if guess in ('q', 'quit', 'exit', 'back'):
                print(f"{Fore.LIGHTBLACK_EX}The number was {number}. Exiting the game...{Fore.RESET}\n")
                break

            guess = int(guess)

            if guess < 1 or guess > 100:
                print(f"{Fore.RED}Please enter a number between 1 and 100.{Fore.RESET}")
                attempts -= 1
                continue

            if guess == number:
                print(
                    f"{Fore.GREEN}Congratulations! You guessed the number {number} in {attempts} attempts!{Fore.RESET}")
                break
            elif guess < number:
                print(f"Too low! {attempts_left} attempts remaining.")
            else:
                print(f"Too high! {attempts_left} attempts remaining.")

        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Fore.RESET}")
            attempts -= 1
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTBLACK_EX}Game interrupted. The number was {number}.{Fore.RESET}\n")
            return

    if attempts > max_attempts:
        print(f"{Fore.RED}Game over! The number was {number}. Better luck next time!{Fore.RESET}")


def rock_paper_scissors():
    """
    Rock Paper Scissors game logic.
    Player competes against the computer in classic hand game.
    """
    choices = ["rock", "paper", "scissors"]
    wins = 0
    losses = 0
    ties = 0

    print(f"\n{Fore.CYAN}Rock Paper Scissors Game")
    print(f"Type 'rock', 'paper', or 'scissors' to play.")

    while True:
        try:
            player_choice = input(f"{Fore.YELLOW}Your choice (rock/paper/scissors): {Fore.RESET}").strip().lower()

            if player_choice in ('q', 'quit', 'exit', 'back'):
                print(f"{Fore.LIGHTBLACK_EX}Exiting the game...{Fore.RESET}\n")
                break

            if player_choice not in choices:
                print(f"{Fore.RED}Invalid choice. Please enter 'rock', 'paper', or 'scissors'.{Fore.RESET}")
                continue

            computer_choice = random.choice(choices)

            print(f"{Fore.WHITE}You chose: {player_choice}")
            print(f"Computer chose: {computer_choice}")

            if player_choice == computer_choice:
                print(f"{Fore.YELLOW}It's a tie!{Fore.RESET}")
                ties += 1
            elif (player_choice == "rock" and computer_choice == "scissors") or \
                    (player_choice == "paper" and computer_choice == "rock") or \
                    (player_choice == "scissors" and computer_choice == "paper"):
                print(f"{Fore.LIGHTGREEN_EX}You win: {player_choice} beats {computer_choice}!{Fore.RESET}")
                wins += 1
            else:
                print(f"{Fore.LIGHTRED_EX}You lose: {computer_choice} beats {player_choice}!{Fore.RESET}")
                losses += 1

            print(f"{Fore.CYAN}Score: {wins} wins, {losses} losses, {ties} ties{Fore.RESET}.\n")

        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTBLACK_EX}Game interrupted.{Fore.RESET}")
            break
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")


# Placeholder for Tic-Tac-Toe (to be implemented later)
def tic_tac_toe():
    """Tic-Tac-Toe game (to be implemented)"""
    print(f"\n{Fore.YELLOW}Tic-Tac-Toe game is coming soon!{Fore.RESET}")
    print(f"{Fore.CYAN}This feature is currently under development...{Fore.RESET}")


GAMES = {
    "1": {
        "name": "guess_number",
        "title": "Guess the Number",
        "description": "Try to guess a randomly generated number between 1 and 100.",
        "function": guess_number
    },
    "2": {
        "name": "rock_paper_scissors",
        "title": "Rock Paper Scissors",
        "description": "Classic hand game against the computer.",
        "function": rock_paper_scissors
    },
    "3": {
        "name": "tic_tac_toe",
        "title": "Tic-Tac-Toe",
        "description": "Classic 3x3 tic-tac-toe against the computer (coming soon).",
        "function": tic_tac_toe
    }
}

# Alternative names for quick access
GAME_ALIASES = {
    "guess": "1",
    "number": "1",
    "rock": "2",
    "paper": "2",
    "scissors": "2",
    "rps": "2",
    "tic": "3",
    "tac": "3",
    "tictactoe": "3"
}


def show_games_list():
    """Display list of all available games"""
    print(f"\n{Fore.CYAN}Available games:{Fore.RESET}")
    for game_id, game_info in GAMES.items():
        print(f"{Fore.YELLOW}{game_id}. {game_info['title']}{Fore.RESET}")
        print(f"   {game_info['description']}")
        print(f"   {Fore.LIGHTBLACK_EX}Command: {game_info['name']}{Fore.RESET}")
    print("\nTo quit any game, type 'q'.\n")
    print("To view abbreviated names for games, type 'abbr'.\n")


def get_game_by_input(user_input):
    """
    Find game by user input (number or name)
    Returns game information or None if not found
    """
    user_input = user_input.lower().strip()

    # Search by number
    if user_input in GAMES:
        return GAMES[user_input]

    # Search by aliases
    if user_input in GAME_ALIASES:
        game_id = GAME_ALIASES[user_input]
        return GAMES[game_id]

    # Search by full name
    for game_id, game_info in GAMES.items():
        if game_info["name"] == user_input:
            return game_info

    return None


def start_game(game_info):
    """Launch selected game"""
    try:
        game_info["function"]()
    except Exception as e:
        print(f"{Fore.RED}Error starting game: {e}{Fore.RESET}")


def start_game_by_input(game_input):
    """
    Quick launch a game by name or number
    :param game_input: game number or name
    """
    game_info = get_game_by_input(game_input)

    if game_info:
        start_game(game_info)
    else:
        print(f"{Fore.RED}Game '{game_input}' not found.{Fore.RESET}")
        print(f"Type {Fore.CYAN}games{Fore.RESET} to see available games.")


def game_mode():
    """
    Interactive game selection mode
    """
    print(f"\n{Fore.CYAN}You are in game mode!{Fore.RESET} Enter game number or name to play.")
    print("Type 'list' to see available games or 'back' to return to main menu.")

    while True:
        try:
            user_input = input(f"{Fore.GREEN}games> {Fore.RESET}").strip().lower()

            if user_input in ('back', 'quit', 'exit', 'return'):
                print(f"{Fore.LIGHTBLACK_EX}Returning to main menu...{Fore.RESET}\n")
                break

            elif user_input in ('list', 'help', '?'):
                show_games_list()

            elif user_input:
                game_info = get_game_by_input(user_input)

                if game_info:
                    start_game(game_info)
                else:
                    print(f"{Fore.RED}Game '{user_input}' not found.{Fore.RESET}")
                    print(f"Type {Fore.YELLOW}list{Fore.RESET} to see available games.")

        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTBLACK_EX}Returning to main menu...{Fore.RESET}")
            break
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}{Fore.RESET}")
