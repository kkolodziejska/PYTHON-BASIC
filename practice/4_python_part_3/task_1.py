"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >> calculate_days('2021-10-05')
    1
    >> calculate_days('10-07-2021')
    WrongFormatException
"""
from datetime import datetime
import pytest


class WrongFormatException(Exception):
    pass


def calculate_days(from_date: str) -> int:
    today_date = datetime.now()
    try:
        custom_date = datetime.fromisoformat(from_date)
    except ValueError:
        raise WrongFormatException("WrongFormatException: "
                                   "enter date in format 'yyyy-mm-dd'")
    return (today_date - custom_date).days


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""


@pytest.mark.parametrize('input_date, expected',
                         [('2021-10-07', -1),
                          ('2021-09-30', 6),
                          ('2021-10-06', 0),
                          ('2022-10-06', -365)])
@pytest.mark.freeze_time
def test_calculate_days_valid_inputs(freezer, input_date, expected):
    freezer.move_to('2021-10-06')
    assert calculate_days(input_date) == expected


@pytest.mark.freeze_time
def test_calculate_days_invalid_input(freezer):
    freezer.move_to('2021-10-06')
    with pytest.raises(WrongFormatException) as e:
        calculate_days('10-09-2021')
    assert 'WrongFormatException' in str(e.value)
