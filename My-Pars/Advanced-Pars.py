import requests
from bs4 import BeautifulSoup
import csv
import re


def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('Викторины.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['number'],
                         data['question'],
                         data['answer']])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find_all('tr', {'class': 'tooltip'})

    for tr in trs:

        tds = tr.find_all('td')

        try:
            number = tds[0].text
        except:
            number = ''
        try:
            question = tds[1].find('a').text
        except:
            question = ''
        try:
            answer = tds[2].text
        except:
            answer = ''

        data = {'number': number,
                'question': question,
                'answer': answer}

        write_csv(data)


def main():
    url = 'https://baza-otvetov.ru/categories'
    get_page_data(get_html(url))
    soup = BeautifulSoup(get_html(url), 'lxml')
    categories = soup.find_all('div', {'class': 'block'})
    for i in categories:
        url1 = i.find('h2').find('a').get('href')

        url = 'https://baza-otvetov.ru' + str(url1)

        while True:
            get_page_data(get_html(url))

            soup = BeautifulSoup(get_html(url), 'lxml')

            try:
                pattern = '>'
                url = 'https://baza-otvetov.ru' + soup.find('div',
                {'class': 'q-list__nav'}).find('a', text=re.compile(pattern)).get('href')
            except:
                break


if __name__ == '__main__':
    main()

