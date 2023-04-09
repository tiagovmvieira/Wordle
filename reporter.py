from typing import List
from colorama import Fore

from wordle import Wordle
from letter_state import LetterState

class Reporter:
    def __init__(self, wordle: Wordle):
        self.wordle = wordle

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
    def _draw_game_board(lines: List[str], size: int = 9, padding: int = 1):
        content_length = size + padding * 2

        top_border = "┌" + "─" * content_length + "┐"
        bottom_border = "└" + "─" * content_length + "┘"
        space = " " * padding

        print(top_border)
        for line in lines:
            print("│" + space + line + space + "│")
        print(bottom_border)

    @staticmethod
    def _draw_keyboard():
        pass

    def display_results(self):
        print("\nYour results so far...")
        print(f"You have {self.wordle.remaining_attempts} attempts remaining.")

        lines = []

        for word in self.wordle.attempts:
            result = self.wordle.guess(word)
            colored_result_str = self._convert_result_to_color(result=result)
            lines.append(colored_result_str)

        for _ in range(self.wordle.remaining_attempts):
            lines.append(" ".join(["_"] * self.wordle.word_length))

        self._draw_game_board(lines=lines)
        self._draw_keyboard()
