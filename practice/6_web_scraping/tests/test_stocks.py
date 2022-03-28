import stock_info
from pytest import mark, fixture
from unittest.mock import patch
import requests
import pickle


@fixture
def requests_session():
    s = requests.Session()
    s.headers = {'Host': 'finance.yahoo.com',
                 'User-Agent': 'python requests 2.27.1'}
    return s


def get_response(filename: str) -> requests.models.Response:
    with open(f'test_responses/{filename}', 'br') as f:
        response = pickle.load(f)
    return response


@patch('requests.sessions.Session.get')
def test_get_results(mocked_get, requests_session):
    mocked_get.return_value = get_response('most_active')
    expected = '246'
    assert stock_info.get_number_of_stocks(requests_session) == expected


@patch('requests.sessions.Session.get')
def test_get_stocks_name_code(mocked_get, requests_session):
    mocked_get.return_value = get_response('most_active')
    expected = [{'Code': 'TLRY', 'Name': 'Tilray Brands, Inc.'},
                {'Code': 'NIO', 'Name': 'NIO Inc.'},
                ]
    assert stock_info.get_stocks_name_code(requests_session, '2') == expected


@patch('requests.sessions.Session.get')
def test_get_stock_52_week_change(mocked_get, requests_session):
    mocked_get.return_value = get_response('PDD_statistics')
    expected = {'52-Week Change': '-66.37%',
                'Total Cash': '92.94B'}
    assert stock_info.get_stock_52_week_change(requests_session, 'PDD') == expected


@patch('requests.sessions.Session.get')
@mark.parametrize('symbol, expected',
                         [('PDD', {'Shares': '20,304,002',
                                   'Date Reported': 'Dec 30, 2021',
                                   '% Out': '1.62%',
                                   'Value': '1,183,723,316'}),
                          ('TLRY', {'Shares': '',
                                    'Date Reported': '',
                                    '% Out': '',
                                    'Value': ''})])
def test_get_stock_holder(mocked_get, symbol, expected, requests_session):
    mocked_get.return_value = get_response(f'{symbol}_holders')
    assert stock_info.get_stock_holder(requests_session, symbol) == expected


@patch('requests.sessions.Session.get')
def test_get_stock_profile(mocked_get, requests_session):
    mocked_get.return_value = get_response('PDD_profile')
    expected = {'Country': 'China',
                'Employees': '',
                'CEO Name': 'Mr. Zhenwei  Zheng',
                'CEO Year Born': '1984'}
    assert stock_info.get_stock_profile(requests_session, 'PDD') == expected
