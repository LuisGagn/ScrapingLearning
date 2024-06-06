from bs4 import BeautifulSoup
import requests

def scrapBlogs():
    pageToScrape = requests.get("https://www.tapaway.com.au/blog")
    soup = BeautifulSoup(pageToScrape.text, "html.parser")
    authors = soup.findAll('span', attrs={'class':'tQ0Q1A'})
    titles = soup.findAll('p', attrs={'class':'bD0vt9 KNiaIk'})
    for title in titles:
        print(title.text)


scrapBlogs()