#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import re


# def test():
#     url = 'https://www.cooky.vn/dia-diem-tai-ha-noi?p=' + str(1)
#     source_code = requests.get(url)
#     plain_text = source_code.text
#     soup = BeautifulSoup(plain_text, 'html.parser')
#     thing = soup.find('div', {'class': 'loc-list-item'})
#     # for thing in all_stores:
#     store = {}
#     store['url'] = 'https://www.cooky.vn' + thing.find('a', {'class': 'photo'}).get('href')
#     store['img'] = thing.find('img').get('data-src')
#     store['type'] = thing.find('div', {'class': 'cat'}).find('a', {
#         'class': 'location-categories'}).text.strip()
#     store['name'] = thing.find('div', {'class': 'info'}).find('h2', {'class': 'name'}).text
#     store['short-desc'] = thing.find('div', {'class': 'short-desc'}).text.strip()
#     store['opening-time'] = thing.find('div', {'class': 'opening-stats'}).find('span',
#                                                                                {'class': 'opening-time'}).text
#     store_soup = BeautifulSoup(requests.get(store['url']).text, 'html.parser')
#     store_rating = store_soup.find('div', {'class': 'rating'}).find_all('div', {'class': 'rating-item'})
#     store['price_rate'] = store_rating[0].find('span', {'class': 'rating-value'}).text
#     store['quality_rate'] = store_rating[1].find('span', {'class': 'rating-value'}).text
#     store['service_rate'] = store_rating[2].find('span', {'class': 'rating-value'}).text
#     print(store['price_rate'])


def url_to_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup


def scrape(pages):
    # location = 'ho-chi-minh'
    location = 'ha-noi'
    data = []
    page = 1
    while page <= pages:
        url = 'https://www.cooky.vn/dia-diem-tai-' + location + '?p=' + str(page)
        soup = url_to_soup(url)
        all_stores = soup.find_all('div', {'class': 'loc-list-item'})
        for thing in all_stores:
            store = dict()
            store['url'] = 'https://www.cooky.vn' + thing.find('a', {'class': 'photo'}).get('href')
            store['img'] = thing.find('img').get('data-src')
            store['type'] = thing.find('div', {'class': 'cat'}).find('a', {
                'class': 'location-categories'}).text.strip()
            store['name'] = thing.find('div', {'class': 'info'}).find('h2', {'class': 'name'}).text
            store['short-desc'] = thing.find('div', {'class': 'short-desc'}).text.strip()
            store['opening-time'] = thing.find('div', {'class': 'opening-stats'}).find('span',
                                                                                       {'class': 'opening-time'}).text

            # the soup store
            store_soup = url_to_soup(store['url'])

            # rating section
            store_rating = store_soup.find('div', {'class': 'rating'})
            price = store_rating.find('span', {'class': 'rating-text'}, string=re.compile('Giá cả'))
            store['price_rate'] = price.find_previous('span', {'class': 'rating-value'}).text if price else None
            quality = store_rating.find('span', {'class': 'rating-text'}, string=re.compile('Chất lượng'))
            store['quality_rate'] = quality.find_previous('span', {'class': 'rating-value'}).text if quality else None
            service = store_rating.find('span', {'class': 'rating-text'}, string=re.compile('Dịch vụ'))
            store['service_rate'] = service.find_previous('span', {'class': 'rating-value'}).text if service else None

            # contact section
            fan_page = store_soup.find('span', string=re.compile('Fanpage'))
            store['fan_page'] = fan_page.find_next('a').text if fan_page else None
            website = store_soup.find('span', string=re.compile('Website'))
            store['website'] = website.find_next('a').text if website else None
            contact = store_soup.find('span', string=re.compile('Liên hệ'))
            store['contact'] = contact.find_next('a').text if contact else None
            store['option'] = [smt.text for smt in store_soup.find('div', {'class': 'options-box row'}).find_all('a')]

            # photos section
            store_photos_url = store['url'] + '/hinh-anh'
            store_photos_soup = url_to_soup(store_photos_url)
            store_photos = store_photos_soup.find('div', {'class': 'photo-list'})
            photos = [photo.get('src') for photo in store_photos.find_all('img')[:-1]] if store_photos else None
            store['photos'] = photos

            # menu section
            store_menu_url = store['url'] + '/menu'
            store_menu_soup = url_to_soup(store_menu_url)
            store_menu = store_menu_soup.find('div', {'class': 'menu-list'})

            menu_checkpoint = store_menu.find('script') if store_menu else None
            store['menu'] = [item.text.strip() for item in menu_checkpoint.find_all_previous('a', {
                'class': 'menu-item'})] if menu_checkpoint else None

            # info section
            store_info_url = store['url'] + '/thong-tin'
            store_info_soup = url_to_soup(store_info_url)
            phone_number = store_info_soup.find('span', string=re.compile('Điện thoại'))
            store['phone_number'] = phone_number.findParent('p').text.strip('Điện thoại:') if phone_number else None

            if store not in data:
                data.append(store)

        page += 1
    with open("dummy.json", 'w') as json_data_out:
        json.dump(data, json_data_out, ensure_ascii=False, indent=2)


# test()
scrape(200)
