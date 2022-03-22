"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import faker
from unittest.mock import patch
import pytest


def print_name_address(args: argparse.Namespace) -> None:
    fake = faker.Faker()
    for _ in range(args.NUMBER):
        arg_dict = dict()
        for arg in vars(args):
            if arg != 'NUMBER':
                arg_dict[arg] = getattr(fake, getattr(args, arg))()
        print(arg_dict)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(usage='NUMBER --FIELD=PROVIDER '
                                     '[--FIELD=PROVIDER ... ]',
                                     add_help=False)
    parser.add_argument("NUMBER", type=int,
                        help="positive number of generated instances")
    parent_args = parser.parse_known_args()
    options = parent_args[1]
    for opt in options:
        opt = opt.split('=')
        parser.add_argument(f'{opt[0]}', default=opt[1], action='store')
    all_args = parser.parse_args()
    return all_args


if __name__ == '__main__':

    input_args = get_args()
    print_name_address(args=input_args)


"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""

INPUTS = [(argparse.Namespace(NUMBER=2, random_name='name'),
           "{'random_name': 'Megan Sutton'}\n"
           "{'random_name': 'Jennifer Cameron'}\n"),
          (argparse.Namespace(NUMBER=2, random_name='name', random_address='address'),
           "{'random_name': 'Megan Sutton', 'random_address': 'this is random address 1'}"
           "\n{'random_name': 'Jennifer Cameron', 'random_address': 'this is random address 2'}\n"),
          (argparse.Namespace(NUMBER=2), '{}\n{}\n'),
          (argparse.Namespace(NUMBER=0), '')]


@pytest.mark.parametrize('input_args, expected', INPUTS)
@patch('faker.providers.person.Provider.name',
       side_effect=['Megan Sutton', 'Jennifer Cameron'])
@patch('faker.providers.address.Provider.address',
       side_effect=['this is random address 1', 'this is random address 2'])
def test_print_name_address(mocked_faker1, mocked_faker2, input_args, expected, capfd):
    print_name_address(input_args)
    out, err = capfd.readouterr()
    assert out == expected
