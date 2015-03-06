__author__ = 'z9764'
import requests
from bs4 import BeautifulSoup

r=requests.get("http://www.oxforddictionaries.com/definition/american_english/hole")

print(r.status_code)

print(r.headers['content-type'])

soup = BeautifulSoup(r.text)


if __name__ == '__main__':
    pass