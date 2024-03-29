from typing import List
from colorama import Fore

from wordle.wordle import Wordle
from wordle.letter_state import LetterState

class Reporter:
    def __init__(self, wordle: Wordle):
        self.wordle = wordle

    def report(self, **kwargs):
        if kwargs.get('initial_message'):
            print(Fore.CYAN + "\nPress ctrl + C to Give Up" + Fore.RESET)
        if kwargs.get('game_configs'):
            print(Fore.GREEN + f"\nGame Mode: " + Fore.RESET + f"{self.wordle._game_mode}\n"
                + Fore.GREEN + "Word Length: " + Fore.RESET + f"{self.wordle.word_length}")
        if kwargs.get('characters_exceeded'):
            print(Fore.RED + f"Word must be {self.wordle.word_length} characters long!" + Fore.RESET)
        elif kwargs.get('word_not_found'):
            print(Fore.RED + "Word provided does not exist in the English dictionary." + Fore.RESET)
        elif kwargs.get('final_message'):
            print(f"You've solved the puzzle in {self.wordle.taken_attempts} attempts!") if self.wordle.is_solved\
                else print(f"\nYou failed to solve the puzzle\nThe answer was {Fore.CYAN + self.wordle.instance_secret + Fore.RESET}.")
        elif kwargs.get('give_up'):
            print("\n\nYou Gave Up!")
            print(f"The answer was {self.wordle.instance_secret}.")
            if self.wordle.attempts:
                self.display_results(give_up=True)
            print("Exiting...")

    def _convert_result_to_color(self, result: List[LetterState])-> str:
        result_with_color = []

        for letter in result:
            if letter.is_in_position:
                color = Fore.GREEN
            elif letter.is_in_word:
                color = Fore.YELLOW
            else:
                color = Fore.WHITE
            
            colored_letter = color + letter.character + Fore.RESET
            result_with_color.append(colored_letter)

        return " ".join(result_with_color)

    @staticmethod
    def _draw_game_board(lines: List[str], word_length: int,  size: int = 9, padding: int = 1):
        content_length = (size + padding * 2) * word_length // 5

        top_border = "┌" + "─" * content_length + "┐"
        bottom_border = "└" + "─" * content_length + "┘"
        space = " " * padding

        print(top_border)
        for line in lines:
            print("│" + space + line + space + "│")
        print(bottom_border)

    @staticmethod
    def _draw_keyboard(keyboard: List[dict]):
        for row in keyboard:
            print(' '.join(row.values()))

    def display_results(self, give_up=False):
        if not give_up:
            print("\nYour results so far...")
            print(f"You have {self.wordle.remaining_attempts} attempts remaining.")

        lines = []

        for word in self.wordle.attempts:
            result = self.wordle.guess(word)
            colored_result_str = self._convert_result_to_color(result=result)
            self.wordle.update_keyboard(result=result)
            lines.append(colored_result_str)

        for _ in range(self.wordle.remaining_attempts):
            lines.append(" ".join(["_"] * self.wordle.word_length))

        print('\n')
        if not give_up:
            print(f'- Attempt {self.wordle.taken_attempts} -')
        Reporter._draw_game_board(lines=lines, word_length=self.wordle.word_length)
        print('\n')
        Reporter._draw_keyboard(keyboard=self.wordle.keyboard)
        print('-------------')
