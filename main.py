# -*- coding: utf-8-sig-*-
import requests
from bs4 import BeautifulSoup
import csv



def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)

def write_csv(data):
    with open('avito.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['metro'],
                         data['url']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_="item_table-description")

    for ad in ads:
        if 'htc' in ad.find('div', class_='item_table-header').find('h3').text.strip().lower():
            try:
                title = ad.find('div', class_='item_table-header').find('h3').text.strip()
            except:
                title = 'Не указано'
            try:
                url = 'https://www.avito.ru' + ad.find('div', class_='item_table-header').find('a').get('href')
            except:
                url = 'Не указана'

            try:
                price = ad.find('div', class_='about').find('span', class_='price').text.strip()
            except:
                price = "Не указана"

            try:
                metro = ad.find('div', class_='data').find('p').text
            except:
                metro = "Не указано"

            data = {
                'title': title,
                'price': price,
                'metro': metro,
                'url': url,
            }
            write_csv(data)
        else:
            continue




def main():
    url = 'https://www.avito.ru/moskva/telefony/htc?p=1&q=htc'
    base_url = 'https://www.avito.ru/moskva/telefony/htc?'
    page_part = 'p='
    query_part = '&q=htc'
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages+1):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)





if __name__ == "__main__":
    main()