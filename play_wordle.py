import sys
import argparse

from dotenv import load_dotenv

from wordle.wordle import Wordle
from wordle.reporter import Reporter

def main():
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Wordle Game CLI")
        parser.add_argument("--word_length", type=int,
                            help="The length of the word to be guessed (default: %(default)s)",
                            choices=range(5, 11), default=5, metavar='[5-10]')
        parser.add_argument("--game_mode", type=str,
                            help="The game mode to play",
                            choices=["single_player", "multi_player"],
                            required=True)
        return parser.parse_args()

    args = parse_arguments()
    load_dotenv()

    print("Hello Wordle!")
    wordle = Wordle(word_length=args.word_length, game_mode=args.game_mode)
    reporter = Reporter(wordle=wordle)
    
    reporter.report(game_configs=True)
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