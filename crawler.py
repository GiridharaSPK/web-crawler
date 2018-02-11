from bs4  import BeautifulSoup
import requests
# import nltk

str="http://www.google.com"

soup = BeautifulSoup(requests.get(str).text,"lxml")
for link in soup.find_all('a'):
    print(link.get('href'))
