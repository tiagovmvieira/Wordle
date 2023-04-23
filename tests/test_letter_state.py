import pytest

from letter_state import LetterState

@pytest.fixture
def letter_state():
    return LetterState('a')

def test_letter_state_initialization(letter_state):
    assert letter_state.character == "a"
    assert letter_state.is_in_word == False
    assert letter_state.is_in_position == False

def test_repr(letter_state):
    assert repr(letter_state) == "a is in word: False, is in position: False"
