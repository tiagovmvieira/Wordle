import sys
import maskpass
import requests

from typing import List
from colorama import Fore

from letter_state import LetterState


class Wordle:
    _max_number_of_attempts = 6
    word_length = 5
    _dictionary_api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    _dictionary_api_headers = {
        "Accept": "application/json"
    }

    def __init__(self):
        self.session = requests.Session()

        self.secret : str = self._get_secret_word()
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
            letter.is_in_word = character in self.secret 
            letter.is_in_position = character == self.secret[i]

            result.append(letter)

        return result

    def set_word_to_check(self, word: str)-> None:
        self.word_to_check: str = word

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

    @property
    def word_exist(self)-> bool:
        if not self.word_to_check:
            return False 

        r = self.session.request(
            url=self._dictionary_api_url + self.word_to_check,
            method="GET",
            headers=self._dictionary_api_headers
        )

        return False if r.status_code != 200 else True


