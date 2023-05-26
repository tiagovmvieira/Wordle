import os
import sys
import maskpass
import requests

from typing import List
from colorama import Fore
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from wordle.letter_state import LetterState
from wordle.api_client import APIClient


class Wordle:
    _max_number_of_attempts = 6
    
    keyboard = [
        {'Q': 'Q', 'W': 'W', 'E': 'E', 'R': 'R', 'T': 'T', 'Y': 'Y', 'U': 'U', 'I': 'I', 'O': 'O', 'P': 'P'},
        {'A': 'A', 'S': 'S', 'D': 'D', 'F': 'F', 'G': 'G', 'H': 'H', 'J': 'J', 'K': 'K', 'L': 'L', 'Ç': 'Ç'},
        {'Z': 'Z', 'X': 'X', 'C': 'C', 'V': 'V', 'B': 'B', 'N': 'N', 'M': 'M'}
    ]

    def __init__(self, word_length: int, game_mode: str):
        self._word_length = word_length
        self._game_mode = game_mode

        self.dictionary_api_client = APIClient(
            base_url="https://api.dictionaryapi.dev/api/v2/entries/en/",
            api_headers = {
                "Accept": "application/json"
            }
        )

        if self._game_mode == "single_player":
            self.secret_generator_api_client = APIClient(
                base_url="https://api.wordnik.com/v4",
                api_headers = {
                    "api_key": os.environ.get('API_KEY')
                }
            )

        self._secret : str = self._get_secret_word()
        self.attempts : list = []

    def _get_secret_word(self)-> str:
        while True:
            try:
                if self._game_mode == "single_player":
                    try:
                        self.word_to_check: str = self.secret_generator_api_client.request(
                            method="GET",
                            endpoint="/words.json/randomWord",
                            params= {
                                    "hasDictionaryDef": "true",
                                    "minLength": str(self._word_length),
                                    "maxLength": str(self._word_length)
                            }
                        ).json().get('word').upper()
                    except (HTTPError, ConnectionError, Timeout, RequestException) as error:
                        raise SystemError(f"Error on the API request - {error}")
                else:
                    self.word_to_check: str = maskpass.askpass(prompt="Enter the Secret Word: ", mask="*").upper()

                if len(self.word_to_check) != self.word_length:
                    print(Fore.RED + f"Secret word must be {self.word_length} characters long!" + Fore.RESET)
                elif self._game_mode == "multi_player" and not self.word_exist:
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
    def word_length(self)-> int:
        return self._word_length

    @property
    def game_mode(self)-> str:
        return self._game_mode

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

        try:
            r = self.dictionary_api_client.request(
                method="GET",
                endpoint=self.word_to_check
            )

            return True
        except HTTPError:
            return False
        except (ConnectionError, Timeout, RequestException) as error:
            raise SystemError(f"Error on the API request - {error}")