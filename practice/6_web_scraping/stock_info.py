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
from bs4 import BeautifulSoup as bsoup
import requests
import re


def get_stocks_info() -> list:
    headers = {'Host': 'finance.yahoo.com',
               'User-Agent': 'python requests 2.27.1'}  # IS IT GOOD PRACTISE TO CHANGE THIS?
    s = requests.Session()
    s.headers = headers

    number_of_stocks = get_number_of_stocks(s)
    all_stocks = get_stocks_name_code(s, number_of_stocks)

    for stock in all_stocks:
        stock_symbol = stock['Code']
        stock.update(get_stock_profile(s, stock_symbol))
        stock.update(get_stock_holder(s, stock_symbol))
        stock.update(get_stock_52_week_change(s, stock_symbol))

    s.close()
    return all_stocks


def get_number_of_stocks(s: requests.Session) -> str:
    url = 'https://finance.yahoo.com/most-active'
    response = s.get(url)
    soup = bsoup(response.text, features='html.parser')

    results = soup.find('span', string=re.compile('results')).text.split()[2]
    return results


def get_stocks_name_code(s: requests.Session, count: str = '25') -> list:
    url = 'https://finance.yahoo.com/most-active'
    response = s.get(url, params={'count': count, 'offset': '0'})
    soup = bsoup(response.text, features='html.parser')

    all_stocks = [{'Code': symbol.text, 'Name': symbol.a['title']} for symbol
                  in soup.find_all("td", attrs={'aria-label': 'Symbol'})]

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

    return {'Country': country_name,
            'Employees': employees,
            'CEO Name': youngest_ceo,
            'CEO Year Born': newest_year}


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


def write_5_youngest_ceos(stock_list: list) -> None:
    stocks_sorted = sorted(stock_list, key=lambda x: x['CEO Year Born'],
                           reverse=True)[:5]
    headers = ['Name', 'Code', 'Country', 'Employees',
               'CEO Name', 'CEO Year Born']
    title = '5 stocks with youngest CEOs'
    filename = '5_stocks_with_youngest_CEOs'
    write_sheet_to_file(headers, stocks_sorted, title, filename)


def write_10_best_52_week_change(stock_list: list) -> None:
    stocks_sorted = sorted(stock_list,
                           key=lambda x: float(x['52-Week Change'].strip('%')),
                           reverse=True)[:10]
    headers = ['Name', 'Code', '52-Week Change', 'Total Cash']
    title = '10 stocks with best 52-Week Change'
    filename = '10_stocks_with_best_52-Week_Change'
    write_sheet_to_file(headers, stocks_sorted, title, filename)


def write_10_blackrock_holds(stock_list: list) -> None:
    stocks_sorted = [stock for stock in stock_list
                     if stock['Shares'] != ''][:10]
    stocks_sorted.sort(key=lambda x: int(x['Shares'].replace(',', '')),
                       reverse=True)
    headers = ['Name', 'Code', 'Shares', 'Date Reported', '% Out', 'Value']
    title = '10 largest holds of Blackrock Inc.'
    filename = '10_largest_holds_of_Blackrock_Inc'
    write_sheet_to_file(headers, stocks_sorted, title, filename)


def write_sheet_to_file(headers: list, data: list,
                        title: str, filename: str) -> None:
    lens = []
    for header in headers:
        column_lens = [len(stock[header]) for stock in data]
        column_lens.append(len(header))
        lens.append(max(column_lens))
    line_length = sum(lens) + len('/ ') * 2 + len(' / ') * (len(headers) - 1)
    print_format = '/ ' + ' / '.join(['{:<' + str(l) + '}' for l in lens]) + ' /'

    with open(f'{filename}.txt', 'w') as f:
        print(f' {title} '.center(line_length, '='), file=f)
        print(print_format.format(*headers), file=f)
        print('-' * line_length, file=f)
        for stock in data:
            print(print_format.format(*[stock[key] for key in headers]), file=f)


def main() -> None:
    stocks = get_stocks_info()
    write_5_youngest_ceos(stocks)
    write_10_best_52_week_change(stocks)
    write_10_blackrock_holds(stocks)


if __name__ == '__main__':
    main()
