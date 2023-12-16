import pytest
import maskpass

from colorama import Fore

from wordle.wordle import Wordle
from wordle.reporter import Reporter

@pytest.fixture
def valid_wordle(monkeypatch):
    secret = "apple"
    monkeypatch.setattr(maskpass, 'askpass', lambda prompt, mask: secret)
    return Wordle()

@pytest.fixture
def reporter(valid_wordle):
    return Reporter(wordle=valid_wordle)

def test_reporter_report_initial_message(capsys, reporter):
    reporter.report(initial_message=True)
    captured = capsys.readouterr()
    assert captured.out == f"{Fore.CYAN}\nPress ctrl + C to Give Up{Fore.RESET}\n"

def test_reporter_report_characters_exceeded(capsys, reporter):
    reporter.report(characters_exceeded=True)
    captured = capsys.readouterr()
    assert captured.out == f"{Fore.RED}Word must be {reporter.wordle.word_length} characters long!{Fore.RESET}\n"

def test_reporter_report_word_not_found(capsys, reporter):
    reporter.report(word_not_found=True)
    captured = capsys.readouterr()
    assert captured.out == f"{Fore.RED}Word provided does not exist in the English dictionary.{Fore.RESET}\n"

def test_reporter_report_final_message_solved(capsys, reporter, valid_wordle):
    valid_wordle.attempt('score')
    valid_wordle.attempt('score')
    valid_wordle.attempt('score')
    valid_wordle.attempt('apple')

    reporter.report(final_message=True)
    captured = capsys.readouterr()
    assert captured.out == "You've solved the puzzle in 4 attempts!\n"

def test_reporter_report_final_message_not_solved(capsys, reporter):
    reporter.report(final_message=True)
    captured = capsys.readouterr()
    assert captured.out == f"You failed to solve the puzzle\nThe answer was {Fore.CYAN}{reporter.wordle.instance_secret}{Fore.RESET}.\n"
