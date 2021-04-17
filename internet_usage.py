import re
import os
from requests import Session
from bs4 import BeautifulSoup

limit = '500.00'

print('Fetching usage...\n')

with Session() as s:
    home_page = 'https://secure.internode.on.net/'
    login_page = 'https://secure.internode.on.net/myinternode/sys0/login'
    website = s.get(login_page)

    soup = BeautifulSoup(website.content, 'html.parser')
    
    login_data = {'username':
                  'sakalmon@internode.on.net',
                  'password':
                  'fEtre.7c'}

    s.post(login_page,
           login_data)
    menu = s.get(login_page)
    soup = BeautifulSoup(menu.content, 'html.parser')

    a_tags = soup.find_all('a')
    
    link_regex = re.compile(r'/myinternode/sys2/adslstats')

    try:
        for tag in a_tags:
            if link_regex.search(tag.get('href')):
                usage_link = home_page + tag.get('href')[1:]
                break
    except:
        pass

    usage_page = s.get(usage_link)
    soup = BeautifulSoup(usage_page.content, 'html.parser')
    td = soup.find_all('td', attrs={'class': 'cell-bg-blue'})
    
    line = td[1]

    data_regex = re.compile(r'(\d)*.\d')
    match = data_regex.search(line.text)
    data_used = match.group(0)
    data_used = round(float(data_used) / 1000, 2)
    remaining = round(float(limit) - float(data_used), 2)
    # TODO - Tidy up the following lines by creating new variables.
    print(f'{"Used: ".ljust(11)}{str(data_used).rjust(6)}GB')
    print(f'{"Limit: ".ljust(11)}{limit.rjust(6)}GB')
    print(f'{"Remaining: ".ljust(11)}{str(remaining).rjust(6)}GB')

    print()
    input('Press enter to exit...')
