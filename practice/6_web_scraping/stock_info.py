"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO
    info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
import pytest
from bs4 import BeautifulSoup as bsoup
import requests
import re
import unittest.mock
from pytest import mark


def get_stocks_info() -> dict:
    headers = {'Host': 'finance.yahoo.com',
               'User-Agent': 'python requests 2.27.1'}  # IS IT GOOD PRACTISE TO CHANGE THIS?
    s = requests.Session()
    s.headers = headers

    number_of_stocks = get_number_of_stocks(s)

    all_stocks = get_all_stocks(s, number_of_stocks)

    for stock_symbol in all_stocks:

        all_stocks[stock_symbol].update(get_stock_profile(s, stock_symbol))
        all_stocks[stock_symbol].update(get_stock_holder(s, stock_symbol))
        all_stocks[stock_symbol].update(get_stock_52_week_change(s, stock_symbol))

    s.close()

    return all_stocks


# TODO: REWRITE 3 FUNCTIONS UNDER AND SAVE DATA TO FILE
def get_5_youngest_ceos():
    stocks = get_stocks_info()
    stocks_sorted = sorted(stocks.items(), key=lambda x: x[1]['ceo_born'],
                           reverse=True)[:5]
    return stocks_sorted


def get_10_best_52_week_change():
    stocks = get_stocks_info()
    stocks_sorted = sorted(stocks.items(),
                           key=lambda x: float(x[1]['52-Week Change'].strip('%')),
                           reverse=True)[:10]
    return stocks_sorted


def get_10_blackrock_holds():
    stocks = get_stocks_info()
    stocks_sorted = sorted(stocks.items(),
                           key=lambda x: int(x[1]['Shares'].replace(',', ''))
                           if x[1]['Shares'] != '' else 0, reverse=True)[:10]
    return stocks_sorted


def get_number_of_stocks(s: requests.Session) -> str:
    url = 'https://finance.yahoo.com/most-active'
    response = s.get(url)
    soup = bsoup(response.text, features='html.parser')

    results = soup.find('span', string=re.compile('results')).text.split()[2]
    return results


def get_all_stocks(s: requests.Session, count: str = '25') -> dict:
    url = 'https://finance.yahoo.com/most-active'
    response = s.get(url, params={'count': count, 'offset': '0'})
    soup = bsoup(response.text, features='html.parser')

    all_stocks = {symbol.text: {'Name': symbol.a['title']} for symbol
                  in soup.find_all("td", attrs={'aria-label': 'Symbol'})}

    return all_stocks


def get_stock_profile(s: requests.Session, symbol: str) -> dict:
    url = f'https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}'
    response = s.get(url)
    soup = bsoup(response.text, features='html.parser')

    country_name = soup.find('p', class_='D(ib) W(47.727%) Pend(40px)')\
        .get_text('\n').split('\n')[-3]
    employees = soup.find('span', string='Full Time Employees')\
        .find_next_sibling('span').text
    newest_year = max([year.text for year
                       in soup.find_all('td', class_='Ta(end)')[2::3]
                       if year.text != 'N/A'])
    youngest_ceo = soup.find('span', string=newest_year).find_parent('td')\
        .find_previous_siblings('td', class_='Ta(start)')[-1].text

    return {'country_name': country_name,
            'employees': employees,
            'youngest_ceo': youngest_ceo,
            'ceo_born': newest_year}


def get_stock_holder(s: requests.Session, symbol: str) -> dict:
    url = f'https://finance.yahoo.com/quote/{symbol}/holders?p={symbol}'
    response = s.get(url)
    soup = bsoup(response.text, features='html.parser')

    try:
        holder_info = [info.text for info
                       in soup.find('td', string='Blackrock Inc.')
                           .find_next_siblings('td')]
    except AttributeError:
        holder_info = ['', '', '', '']

    holder_keys = ['Shares', 'Date Reported', '% Out', 'Value']

    return dict(zip(holder_keys, holder_info))


def get_stock_52_week_change(s: requests.Session, symbol: str) -> dict:
    url = f'https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}'
    response = s.get(url)
    soup = bsoup(response.text, features='html.parser')

    week_change = soup.find('span', string='52-Week Change').find_parent('td')\
        .find_next_sibling('td').text
    total_cash = soup.find('span', string='Total Cash').find_parent('td')\
        .find_next_sibling('td').text

    return {'52-Week Change': week_change,
            'Total Cash': total_cash}

# --------------------------------- TESTS --------------------------------------


@pytest.fixture
def requests_session():
    s = requests.Session()
    s.headers = {'Host': 'finance.yahoo.com',
                 'User-Agent': 'python requests 2.27.1'}
    return s


def test_get_results(requests_session):
    expected = '246'
    assert get_number_of_stocks(requests_session) == expected


def test_get_all_stocks(requests_session):
    expected = {'TLRY': {'Name': 'Tilray Brands, Inc.'},
                'NIO': {'Name': 'NIO Inc.'},
                }
    assert get_all_stocks(requests_session, '2') == expected


def test_get_stock_52_week_change(requests_session):
    expected = {'52-Week Change': '-66.37%',
                'Total Cash': '92.94B'}
    assert get_stock_52_week_change(requests_session, 'PDD') == expected


@mark.parametrize('symbol, expected',
                         [('PDD', {'Shares': '20,304,002',
                                   'Date Reported': 'Dec 30, 2021',
                                   '% Out': '1.62%',
                                   'Value': '1,183,723,316'}),
                          ('TLRY', {'Shares': '',
                                    'Date Reported': '',
                                    '% Out': '',
                                    'Value': ''})])
def test_get_stock_holder(symbol, expected, requests_session):
    assert get_stock_holder(requests_session, symbol) == expected


def test_get_stock_profile(requests_session):
    expected = {'country_name': 'China',
                'employees': '',
                'youngest_ceo': 'Mr. Zhenwei  Zheng',
                'ceo_born': '1984'}
    assert get_stock_profile(requests_session, 'PDD') == expected


@unittest.mock.patch('stock_info.get_number_of_stocks', return_value='5')
def test_get_5_youngest_ceos(mocked_number):
    expected = {'TLRY': {
        'Name': 'Tilray Brands, Inc.',
        'country_name': 'United States',
        'employees': '1,800',
        'youngest_ceo': 'Ms. Denise Menikheim Faltischek',
        'ceo_born': '1973',
        'Shares': '',
        'Date Reported': '',
        '% Out': '',
        'Value': '',
        '52-Week Change': '-60.43%',
        'Total Cash': '331.78M'
    },
        'NIO': {
            'Name': 'NIO Inc.',
            'country_name': 'China',
            'employees': '',
            'youngest_ceo': 'Mr. Wei  Feng',
            'ceo_born': '1981',
            'Shares': '64,036,975',
            'Date Reported': 'Dec 30, 2021',
            '% Out': '4.78%',
            'Value': '2,028,691,368',
            '52-Week Change': '-43.93%',
            'Total Cash': ''
        }
    }

    assert get_10_blackrock_holds() == expected
