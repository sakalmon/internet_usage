import re
import os
from datetime import date
from requests import Session
from bs4 import BeautifulSoup


def get_usage():
    limit = 500.00

    with Session() as s:
        home_page = 'https://secure.internode.on.net/'
        login_page = 'https://secure.internode.on.net/myinternode/sys0/login'
        website = s.get(login_page)

        soup = BeautifulSoup(website.content, 'html.parser')
        
        login_data = {'username':
                      os.environ['INTERNODE_USERNAME'],
                      'password':
                      os.environ['INTERNODE_PASSWORD']}

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

        usage = dict()

        data_regex = re.compile(r'(\d)*.\d')
        match = data_regex.search(line.text)
        data_used = match.group(0)
        data_used = round(float(data_used) / 1000, 2)
        data_used_perc = round((data_used / limit) * 100)
        remaining = round(float(limit) - float(data_used), 2)
        usage['used'] = data_used
        usage['used_perc'] = data_used_perc
        usage['limit'] = limit
        usage['remaining'] = remaining

        today = date.today()

        if today.day >= 9:
            reset_date = date(today.year, today.month + 1, 9)

        else:
            reset_date = date(today.year, today.month, 9)

        days_remaining = (reset_date - today).days

        usage['days_remaining'] = days_remaining

        print(usage['used'])

        return usage
