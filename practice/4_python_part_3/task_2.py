"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >> math_calculate('log', 1024, 2)
     10.0
     >> math_calculate('ceil', 10.7)
     11
"""
import math
import pytest


class OperationNotFoundException(Exception):
    pass


def math_calculate(function: str, *args):
    try:
        result = getattr(math, function)(*args)
    except AttributeError:
        raise OperationNotFoundException
    else:
        return result


"""
Write tests for math_calculate function
"""


@pytest.mark.parametrize('expected, func, args', [(10.0, 'log', (1024, 2)),
                                                  (11, 'ceil', (10.7,))])
def test_math_calculate_valid_function(expected, func, args):
    assert math_calculate(func, *args) == expected


def test_math_calculate_invalid_function():
    with pytest.raises(OperationNotFoundException) as e:
        math_calculate('foo', 1, 2)
    assert 'OperationNotFoundException' in str(e.type)
