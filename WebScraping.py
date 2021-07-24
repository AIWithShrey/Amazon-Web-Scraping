import requests
import bs4
import pandas as pd
from requests.api import request
import wikipedia
from pprint import PrettyPrinter, pprint
import matplotlib.pyplot as plt
import seaborn as sns

ourdata = requests.get("https://en.wikipedia.org/wiki/Artificial_intelligence")

bsp = bs4.BeautifulSoup(ourdata.text,'lxml')

titles_class=bsp.select('.mw-headline')
'''
for i in titles_class:
    print(i.text)

imgs = bsp.select('img')

for i in imgs:
    print(i)
'''

ai = wikipedia.page(wikipedia.search('Artificial intelligence')[0])

#pprint(ai.links)

#web scraping a book store: books.toscrape.com

pages=[]
prices=[]
ratings=[]
title=[]
urls=[]

number_of_pages = 2

for i in range(1, number_of_pages+1):
    url = ("http://books.toscrape.com/catalogue/page-{}.html".format(i))

    pages.append(url)

for item in pages:
    page = requests.get(item)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

for t in soup.findAll('h3'):
    titless=t.getText()
    title.append(titless)

for p in soup.find_all('p', class_='price_color'):
    price=p.getText()
    prices.append(price)

for s in soup.find_all('p', class_='star-rating'):
    for k,v in s.attrs.items():
        star=v[1]
        ratings.append(star)
        #print(ratings)

divs=soup.find_all('div',class_='image_container') #fetching all the div tags in the class called image_container
#print(divs)

for thumbs in divs:
    tagss=thumbs.find('img',class_='thumbnail')
    #print(tagss)
    links='http://books.toscrape.com/' + str(tagss['src'])
    newlinks=links.replace('..','') #to get rid of the three-dost, u can check it in your browser to see if we ignore it, the link still works, besides ignoring it makes the link more readable
    urls.append(newlinks) #our url list now contains all of the urls of the book images


web_data = {'Title':title, 'Price':prices, 'Ratings':ratings,'URL':urls}
'''
print(len(title))
print(len(prices))
print(len(ratings))
print(len(urls))
'''

df = pd.DataFrame(web_data)
df.index += 1

df['Price']=df['Price'].str.replace('Â£','')
df.sort_values(by='Price',ascending=False, inplace = True)
df['Ratings']=df['Ratings'].replace({'Three': 3, 'Two':2, 'One':1, 'Four':4, 'Five':5})
df['Price']=df['Price'].astype(float)

plt.figure(figsize=(5,5))
sns.heatmap(df.corr())
#plt.show()

print(bsp.select('h3 > span'))