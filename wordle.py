import sys
import maskpass

from typing import Union, List
from colorama import Fore

from letter_state import LetterState


class Wordle:
    _max_number_of_attempts = 6
    word_length = 5

    keyboard = [
        {'Q': "q", 'W': "w", 'E': "e", 'R': "r", 'T': "t", 'y': "y", 'U': "u", 'I': "i", 'O': "o", 'P': "p"},
        {'A': "a", 'S': "s", 'D': "d", 'F': "f", 'G': "g", 'H': "h", 'J': "j", 'K': "k", 'L': "l", 'Ç': "ç"},
        {'Z': "z", 'X': "x", 'C': "c", 'V': "v", 'B': "b", 'N': "n", 'M': "m"}
    ]

    def __init__(self):
        self.secret : str = self._get_secret_word()
        self.attempts : list = []

    def _get_secret_word(self)-> str:
        while True:
            try:
                secret = maskpass.askpass(prompt="Enter the Secret Word: ", mask="*").upper()

                if len(secret) != self.word_length:
                    print(Fore.RED + f"Secret word must be {self.word_length} characters long!" + Fore.RESET)
                elif not secret.isalpha():
                    print(Fore.RED + "Secret word should contain only letters!" + Fore.RESET)
                else:
                    break
            except KeyboardInterrupt:
                print("\n\nSecret Word input cancelled!")
                print("Exiting...")
                sys.exit()

        return secret

    def attempt(self, word: str)-> None:
        word = word.upper()
        self.attempts.append(word)

    def guess(self, word: str)-> List[LetterState]:
        result = []

        for i in range(self.word_length):
            character = word[i]
            letter = LetterState(character=character)
            letter.is_in_word = character in self.secret 
            letter.is_in_position = character == self.secret[i]

            result.append(letter)

        return result

    @property
    def is_solved(self)-> bool:
        return len(self.attempts) > 0 and self.attempts[-1] == self.secret
    
    @property
    def remaining_attempts(self)-> int:
        return self._max_number_of_attempts - len(self.attempts)

    @property
    def taken_attempts(self)-> int:
        return len(self.attempts)

    @property
    def can_attempt(self)-> bool:
        return self.remaining_attempts > 0 and not self.is_solved   



