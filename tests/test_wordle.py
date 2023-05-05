import pytest
import maskpass
from wordle.wordle import Wordle

@pytest.fixture
def valid_wordle(monkeypatch):
    secret = "apple"
    monkeypatch.setattr(maskpass, 'askpass', lambda prompt, mask: secret)
    return Wordle()

def test_word_exist(valid_wordle: Wordle):
    valid_wordle.set_word_to_check("hello")
    assert valid_wordle.word_exist == True

def test_attempt(valid_wordle: Wordle):
    valid_wordle.attempt("hello")
    assert valid_wordle.attempts == ["HELLO"]
    valid_wordle.attempt("world")
    assert valid_wordle.attempts == ["HELLO", "WORLD"]
    valid_wordle.attempt("world")
    assert valid_wordle.attempts == ["HELLO", "WORLD", "WORLD"]

def test_can_attempt(valid_wordle: Wordle):
    setattr(valid_wordle, 'attempts', ['hello', 'score', 'alloy', 'green', 'black'])
    assert valid_wordle.can_attempt == True

    setattr(valid_wordle, 'attempts', ['hello', 'score', 'alloy', 'green', 'black', 'master'])
    assert valid_wordle.can_attempt == False

def test_remaining_attempts(valid_wordle: Wordle):
    setattr(valid_wordle, 'attempts', ['hello'])
    assert valid_wordle.remaining_attempts == 5

def test_is_solved(valid_wordle: Wordle):
    assert valid_wordle.is_solved == False
    
    valid_wordle.attempt('score')
    assert valid_wordle.is_solved == False

    valid_wordle.attempt('apple')
    assert valid_wordle.is_solved == True

def test_taken_attempts(valid_wordle: Wordle):
    valid_wordle.attempt("hello")
    valid_wordle.attempt("world")

    assert valid_wordle.taken_attempts == 2