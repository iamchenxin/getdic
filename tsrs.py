__author__ = 'z9764'
import requests
from bs4 import BeautifulSoup

r=requests.get("http://www.oxforddictionaries.com/definition/american_english/hello")

print(r.status_code)

print(r.headers['content-type'])

soup = BeautifulSoup(r.text)

content = soup.find_all("div",class_="entryPageContent")
print(content.__len__())


if __name__ == '__main__':
    pass