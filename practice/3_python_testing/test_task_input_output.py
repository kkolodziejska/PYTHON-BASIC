"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import patch
from task_input_output import read_numbers


@patch('builtins.input', side_effect=['1', '2', '3', '4'])
def test_read_numbers_without_text_input(mocked_input, capfd):
    read_numbers(4)
    out, err = capfd.readouterr()
    assert out == 'Avg: 2.50\n'


@patch('builtins.input', side_effect=['1', '2', 'Text'])
def test_read_numbers_with_text_input(mocked_input, capfd):
    read_numbers(3)
    out, err = capfd.readouterr()
    assert out == 'Avg: 1.50\n'


@patch('builtins.input', side_effect=['Hello', 'World', 'Text'])
def test_read_numbers_only_text_input(mocked_input, capfd):
    read_numbers(3)
    out, err = capfd.readouterr()
    assert out == 'No numbers entered\n'
