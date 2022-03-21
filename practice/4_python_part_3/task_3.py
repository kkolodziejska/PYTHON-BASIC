"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >> is_http_domain('http://wikipedia.org')
    True
    >> is_http_domain('https://ru.wikipedia.org/')
    True
    >> is_http_domain('griddynamics.com')
    False
"""
import re
import pytest


def is_http_domain(domain: str) -> bool:
    string_pattern = r'https?://(\w+\.\w+)(\.\w+)*(/[\w.]+)*/?\Z'
    matched = re.match(string_pattern, domain)
    if matched:
        return True
    else:
        return False


"""
write tests for is_http_domain function
"""


@pytest.mark.parametrize('tested_string, expected',
                         [('http://pl.wikipedia.org/wiki/Python', True),
                          ('http://pl.wikipedia.org/wiki/Python/', True),
                          ('https://pl.wikipedia.org/wiki/Python', True),
                          ('https://pl.wikipedia.org/wiki/Python/', True),
                          ('https://pl.wikipedia.org/wiki/Python//', False),
                          ('https://pl.wikipedia.org//wiki//Python', False),
                          ('pl.wikipedia.org/wiki/Python/', False),
                          ('http://pl.wikipedia.org/', True),
                          ('http://pl.wikipedia.org', True),
                          ('https://home', False),
                          ('https://home.', False),
                          ('https://home./', False)
                          ])
def test_is_http_domain(tested_string, expected):
    assert is_http_domain(tested_string) == expected
