#!/usr/bin/python3

import locale
from datetime import datetime
from html.parser import HTMLParser
from urllib import request

locale.setlocale(locale.LC_ALL, '')

MUDHEAD_URL = "http://mudhead.se/lt.html"

class Parser(HTMLParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TODAY = datetime.now().strftime('%A').replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
        self.capture_date = False
        self.capture_day_name = False
        self.capture_restaurant = False
        self.capture_dishes = False
        self.services = [
                'http://brickseatery.se/lunch',
                'https://www.fazerfoodco.se/restauranger/restauranger/scotland-yard/'
                ]
        self.days = ['mandag', 'tisdag', 'onsdag', 'torsdag', 'fredag']

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            tag_id = attrs.get('id')
            tag_href = attrs.get('href')
            if tag_id == self.TODAY:
                self.capture_date = True
                self.capture_day_name = True
            elif tag_id in self.days:
                self.capture_date = False
            elif tag_href in self.services:
                self.capture_restaurant = True
        elif tag == 'li':
            self.capture_dishes = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.capture_restaurant = False
            self.capture_dishes = False

        self.capture_day_name = False

    def handle_data(self, data):
        if self.capture_day_name:
            print(data)
            print('=' * len(data))

        if self.capture_date and self.capture_restaurant:
            if self.capture_dishes:
                print(f'\t\u2022 {data}')
            else:
                print(data)
                print('-' * len(data))

def get_body(url):
    response = request.urlopen(url)
    return response.read().decode()

def main():
    body = get_body(MUDHEAD_URL)
    parser = Parser()
    parser.feed(body)
    print('')


if __name__ == "__main__":
    main()
