"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
import urllib.request
import urllib.response
from unittest.mock import Mock, MagicMock, patch, mock_open


def make_request(url: str) -> Tuple[int, str]:
    with urllib.request.urlopen(url) as response:
        code_status = response.status
        response_data = response.read().decode(encoding='utf-8')
    return code_status, response_data


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""


def test_make_request():
    m = MagicMock()
    m.return_value.__enter__.return_value.status = 200
    m.return_value.__enter__.return_value.read.return_value = b'this is some response data'
    with patch('urllib.request.urlopen', m, create=True):
        result = make_request('https://google.com')
    assert result == (200, 'this is some response data')
