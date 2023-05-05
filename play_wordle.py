import sys
import argparse

from wordle.wordle import Wordle
from wordle.reporter import Reporter

def main():
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Wordle Game CLI")
        parser.add_argument("--word_lenght", type=int,
                            help="The length of the word to be guessed (default: %(default)s)",
                            choices=range(5, 11), default=5, metavar='[5-10]')
        return parser.parse_args()

    args = parse_arguments()

    print("Hello Wordle!")
    wordle = Wordle(word_length=args.word_lenght)
    reporter = Reporter(wordle=wordle)
    reporter.report(initial_message=True)

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
            reporter.report(give_up=True)
            sys.exit()

        else:
            wordle.attempt(word)
            reporter.display_results()

    reporter.report(final_message=True)

if __name__ == '__main__':
    main()