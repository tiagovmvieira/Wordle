import sys

from wordle import Wordle
from reporter import Reporter

def main():
    print("Hello Wordle!")
    wordle = Wordle()
    reporter = Reporter(wordle=wordle)

    while wordle.can_attempt:
        try:
            word = input("\nType your guess: ")
            wordle.set_word_to_check(word=word)

            if len(word) != wordle.word_length:
                reporter.report(characters_exceeded=True)
                continue
            elif not wordle.word_exist:
                reporter.report(word_not_found=True)
                continue

        except KeyboardInterrupt:
            print("\n\nGuess input cancelled!")
            print("Exiting...")
            sys.exit()

        else:
            wordle.attempt(word)
            reporter.display_results()

    reporter.report(final_message=True)

if __name__ == '__main__':
    main()