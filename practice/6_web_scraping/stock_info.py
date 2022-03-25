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


# TODO: MAKE FUNCTIONS

STOCKS_URL = 'https://finance.yahoo.com/most-active'
HEADERS = {'Host': 'finance.yahoo.com',
           'User-Agent': 'python requests 2.27.1'}  # IS IT GOOD PRACTISE TO CHANGE THIS?
s = requests.Session()

stocks_response = s.get(STOCKS_URL, headers=HEADERS)
stocks_soup = bsoup(stocks_response.text, features='html.parser')

stocks_dict = dict()

# FIND HOW MANY STOCKS THERE ARE IN GENERAL...
results = stocks_soup.find('span', class_='Mstart(15px) Fw(500) Fz(s)').text
results = (results.split())[2]

# ...AND GET SOUP WITH THEM ALL
stocks_response = s.get(STOCKS_URL, headers=HEADERS,
                        params={'count': results, 'offset': '0'})
stocks_soup = bsoup(stocks_response.text, features='html.parser')

stocks_symbols = [symbol.text for symbol
                  in stocks_soup.find_all("td", attrs={'aria-label': 'Symbol'})]
stocks_names = [name.text for name
                in stocks_soup.find_all("td", attrs={'aria-label': 'Name'})]

for index in range(len(stocks_symbols)):
    stocks_dict[stocks_symbols[index]] = dict()
    stocks_dict[stocks_symbols[index]]['Name'] = stocks_names[index]

del stocks_symbols
del stocks_names

# TODO: FIND YOUNGEST COS - FIND THE YOUNGEST CEO IN EACH STOCK, THEN SORT THEM
for stock_symbol in stocks_dict:
    stock_profile_url = f'https://finance.yahoo.com/quote/{stock_symbol}/profile?p={stock_symbol}'
    stocks_response = s.get(stock_profile_url, headers=HEADERS)
    stock_soup = bsoup(stocks_response.text, features='html.parser')
    # TODO: FIND YOUNGEST CEOS

# GET FULL INFO FROM SELECTED STOCKS
# TODO: ITERATE OVER SELECTED STOCKS
country_name = stock_soup.find('p', class_='D(ib) W(47.727%) Pend(40px)')\
    .get_text('\n').split('\n')[3]
employees = stock_soup.find_all('span', class_='Fw(600)')[2].text
ceo_names = [name.text for name in stock_soup.find_all('td', class_='Ta(start)')[::2]]
ceo_born = [year.text for year in stock_soup.find_all('td', class_='Ta(end)')[2::3]]

s.close()
