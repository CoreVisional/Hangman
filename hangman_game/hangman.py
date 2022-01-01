"""A simple CLI-based Hangman game."""

import os

from typing import Union

from random import choice

from hangman_words import word_list

from hangman_arts import (hangman_stages as stages, hangman_logo)


def ask_user_yes_no(yes_no_question) -> bool:
    """Simplify if/else to determine the correct answers from the user input.

    Args:
        yes_no_question: A string that asks user a yes or no question.

    Returns:
        True if the user's answer is in choice_yes,
        and False otherwise.

        Prints a message to the user if their input are not similar
        to the ones in choice_yes and choice_no.

    """
    choice_yes = ("yes", 'y')
    choice_no = ("no", 'n')

    while True:
        user_choice = input(yes_no_question).lower()

        if user_choice in choice_yes:
            return True

        if user_choice in choice_no:
            return False

        print("\nInvalid Input. Try again.")


def get_random_word() -> str:
    """Select a random word from a list of words.

    Returns:
        A string containing a randomly selected word.

    """
    rand_word = choice(word_list)
    return rand_word


def greet_user() -> None:
    """Display a greeting for the game Hangman."""
    print(hangman_logo)
    print("\033[1m ----- WELCOME TO HANGMAN! -----\033[0m".center(50))


def get_player_names() -> Union[str, tuple[str]]:
    """Ask the user to enter their name.

    Returns:
        A string containing the name of the player.

    This process is repeated until the user
    has provided a valid name.

    """
    greet_user()

    while True:
        player_name = input("\n\nEnter your name: ")

        if not player_name:
            print("\nPlayer Name Required!")
        else:
            return player_name


def get_guess_word() -> str:
    """Ask the player to guess the word one letter at a time.

    Returns:
        A character of the guessed letter.

    This process is repeated until the player has
    provided a valid letter.

    Once the user has keyed in a valid letter, the screen will
    be cleared so that the user will be able to play game
    without drowning in invalid messages.

    """
    while True:
        guess_letter = input("\n\nGuess a letter: ").lower()

        if len(guess_letter) != 1:
            print("\nNo blanks and only a single letter!")
        elif not guess_letter.isalpha():
            print("\nOnly alphabetic characters are allowed!")
        else:
            _ = os.system("clear")
            return guess_letter


class Hangman:
    """Check for the guessed letter and determine the result.

    Hides the word and displays each wrong and correctly guessed letter.
    The result will be shown once the word is guessed or the entire
    hangman is shown.

    Attributes:
        player_name (str): The name of the player.

        chosen_word (str): The chosen word for the user to guess.

        missed_letter (list): Each letter that the user did not guess correctly.

        guessed_letter (list): Each letter the user has guessed correctly.

    """

    def __init__(self) -> None:
        self.player_name = get_player_names()
        self.chosen_word = get_random_word()
        self.missed_letter = []
        self.guessed_letter = []

    def display_letters(self) -> str:
        """Hide the word and display each guessed letter.

        Depending on the length of the the chosen word, each letter
        will be hidden with an underscore and be displayed
        when the user guessed a letter.
        """
        word_result = []

        for char in self.chosen_word:
            if char in self.guessed_letter:
                word_result.append(char)
            elif char == " ":
                word_result.append(" ")
            else:
                word_result.append("_")

        return ' '.join(word_result)

    def check_letters(self) -> None:
        """Check each letter guessed by the user."""
        user_letter = get_guess_word()

        if (user_letter in self.guessed_letter) or (user_letter in self.missed_letter):
            print("\nYou have already guessed that letter!")
        elif (user_letter in self.chosen_word) and (user_letter not in self.guessed_letter):
            self.guessed_letter.append(user_letter)
        elif (user_letter not in self.chosen_word) and (user_letter not in self.missed_letter):
            self.missed_letter.append(user_letter)

    def end_of_game(self) -> bool:
        """Check whether the game has ended or not."""
        if self.check_game_won() or len(self.missed_letter) == 6:
            return True

        return False

    def check_game_won(self) -> bool:
        """Check whether or not the letter is still hidden by an underscore."""
        if "_" not in self.display_letters():
            return True

        return False

    def display_game_status(self) -> None:
        """Display the labels of the game."""
        print(stages[len(self.missed_letter)])
        print(f"\nIncorrect Guesses: {', '.join(self.missed_letter)}")
        print(f"\nLetters Guessed: {', '.join(self.guessed_letter)}")
        print(f"\nSecret Word: {self.display_letters()}")

    def print_game_result(self) -> None:
        """Print the game result and reveal the word."""
        if self.check_game_won():
            print(
                f"\n\nCongratulations, {self.player_name}, you guessed the word!")
        else:
            print(
                f"\n\nYou lost the game, {self.player_name}, Better luck next time!")

        print(f"\nThe word was \033[1m{self.chosen_word}\033[0m.")


def should_play_again() -> bool:
    """Ask the user if they want to play again.

    Returns:
        True if the user wants to play
        again, False otherwise.

    """
    return ask_user_yes_no("\n\nWould you like to play Hangman again? (Y/N): ")


def play_game() -> None:
    """Play hangman game."""
    hangman_game = Hangman()

    while not hangman_game.end_of_game():
        _ = os.system("clear")
        hangman_game.display_game_status()
        hangman_game.check_letters()

    hangman_game.display_game_status()

    hangman_game.print_game_result()


def main():
    """Execute the Hangman program."""
    while True:
        _ = os.system("clear")
        play_game()

        if not should_play_again():
            break

    print("\n\n-----Program Exited-----\n")


if __name__ == "__main__":
    main()
