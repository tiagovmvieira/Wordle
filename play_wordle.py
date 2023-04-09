import sys

from colorama import Fore

from wordle import Wordle
from reporter import Reporter

def main():
    print("Hello Wordle!")
    wordle = Wordle()
    reporter = Reporter(wordle=wordle)

    while wordle.can_attempt:
        try:
            word = input("\nType your guess: ")

            if len(word) != wordle.word_length:
                print(Fore.RED + f"Word must be {wordle.word_length} characters long!" + Fore.RESET)
                continue
            elif not word.isalpha():
                print(Fore.RED + "Your guess should contain only letters!" + Fore.RESET)
                continue

        except KeyboardInterrupt:
            print("\n\nGuess input cancelled!")
            print("Exiting...")
            sys.exit()

        else:
            wordle.attempt(word)
            reporter.display_results()

    print(f"You've solved the puzzle in {wordle.taken_attempts} attempts!") if wordle.is_solved\
        else print("You failed to solve the puzzle")

if __name__ == '__main__':
    main()