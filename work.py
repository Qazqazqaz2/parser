from requests_html import AsyncHTMLSession
import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint
import redis


__all__ = ('work')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


def work():
    jobs = []
    hhh = []
    errors = []
    domain = 'http://www.mojgorod.ru/cities/listcity.html'
    url = domain
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('td', attrs={'width': '70%'})
            main_div = main_div.find('table', attrs={'width': '100%'})
            if main_div:
                div_lst = main_div.find_all('a')
                for div in div_lst:
                    title = div.text
                    title = str(title)
                    print(r.lpush('parser', title))
                    jobs.append(f'<option value="{title}">{title}</option>'
                                f'')
                    hhh = jobs
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
        return hhh, jobs, errors




if __name__ == '__main__':
    jobs = work()
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
