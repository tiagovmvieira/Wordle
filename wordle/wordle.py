import sys
import maskpass
import requests

from typing import List
from colorama import Fore

from wordle.letter_state import LetterState


class Wordle:
    _max_number_of_attempts = 6
    word_length = 5
    _dictionary_api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    _dictionary_api_headers = {
        "Accept": "application/json"
    }
    
    keyboard = [
        {'Q': 'Q', 'W': 'W', 'E': 'E', 'R': 'R', 'T': 'T', 'Y': 'Y', 'U': 'U', 'I': 'I', 'O': 'O', 'P': 'P'},
        {'A': 'A', 'S': 'S', 'D': 'D', 'F': 'F', 'G': 'G', 'H': 'H', 'J': 'J', 'K': 'K', 'L': 'L', 'Ç': 'Ç'},
        {'Z': 'Z', 'X': 'X', 'C': 'C', 'V': 'V', 'B': 'B', 'N': 'N', 'M': 'M'}
    ]

    def __init__(self):
        self.session = requests.Session()

        self._secret : str = self._get_secret_word()
        self.attempts : list = []

    def _get_secret_word(self)-> str:
        while True:
            try:
                self.word_to_check: str = maskpass.askpass(prompt="Enter the Secret Word: ", mask="*").upper()

                if len(self.word_to_check) != self.word_length:
                    print(Fore.RED + f"Secret word must be {self.word_length} characters long!" + Fore.RESET)
                elif not self.word_exist:
                    print(Fore.RED + "Secret word provided does not exist in the English dictionary." + Fore.RESET)
                else:
                    secret = self.word_to_check
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
            letter.is_in_word = character in self._secret 
            letter.is_in_position = character == self._secret[i]

            result.append(letter)

        return result

    def set_word_to_check(self, word: str)-> None:
        self.word_to_check: str = word

    @classmethod
    def update_keyboard(cls, result: List[LetterState]):
        for letter in result:
            if letter.is_in_position:
                color = Fore.GREEN
            elif letter.is_in_word:
                color = Fore.YELLOW
            else:
                color = Fore.RED

            for i, row in enumerate(cls.keyboard):
                if letter.character in row:
                    cls.keyboard[i][letter.character] = f"{color}{letter.character}{Fore.RESET}"

    @property
    def instance_secret(self)-> str:
        return self._secret

    @property
    def is_solved(self)-> bool:
        return len(self.attempts) > 0 and self.attempts[-1] == self._secret
    
    @property
    def remaining_attempts(self)-> int:
        return self._max_number_of_attempts - len(self.attempts)

    @property
    def taken_attempts(self)-> int:
        return len(self.attempts)

    @property
    def can_attempt(self)-> bool:
        return self.remaining_attempts > 0 and not self.is_solved

    @property
    def word_exist(self)-> bool:
        if not self.word_to_check:
            return False 

        r = self.session.request(
            url=self._dictionary_api_url + self.word_to_check,
            method="GET",
            headers=self._dictionary_api_headers
        )

        return False if "message" in r.json() else True