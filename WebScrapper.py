import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas
import csv

url = 'http://olx.in'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
aTags = soup.findAll('a')
hrefTags = [el.get('href') for el in aTags if el.get('href') is not None and el.get('href') != '/']
print(hrefTags,end='\n')

#with open('items.csv',mode='w') as items_file:

 #   items_writer = csv.writer(items_file,delimiter ="|",quotechar='"', quoting=csv.QUOTE_MINIMAL)
images = []
categories = []
itemNames = []
itemPrices = []
categories_to_gather = ['cars','motorcycles','mobile-phones','scooters','pg-guest-houses','furniture','bikes','bicycles','books','gym-fitness','for-rent-houses-apartments','beds-wardrobes']
for tag in hrefTags:
    category = tag.split("_")[0][1:]
    print(category)

    if category not in categories_to_gather:
        continue

    newUrl = url + tag
    # print(newUrl)
    response1 = requests.get(newUrl)
    soup1 = BeautifulSoup(response1.text, "html.parser")
    alist = soup1.find_all('a', href=True)

    # print(type(alist))
    nextLinks = [a['href'] for a in alist if '/item/' in a['href']]
    # print(nextLinks)
    for link in nextLinks:
        nextUrl = url + link
        response2 = requests.get(nextUrl)
        soup2 = BeautifulSoup(response2.text, "html.parser")
        itemPriceTag = soup2.find('span', attrs={'class': '_2xKfz'})
        imageTag = soup2.find('img', attrs={'class': '_3DF4u'})
        print("imageTag:\n", imageTag, end='\n')

        print("itemPriceTag:\n", itemPriceTag, end='\n')
        if imageTag and itemPriceTag:
            imageSrc = imageTag.get('srcset').split(',')[0].split(' ')[0]
            itemName = imageTag.get('alt').split(',')[0]
            itemPrice = itemPriceTag.text.split(' ')[1]
            print('imageSrc', tag, imageSrc, end='\n')
            print('itemName is', itemName, end='\n')
            print("itemPrice:\n", itemPrice, end='\n')
            images.append(imageSrc)
            categories.append(category)
            itemNames.append(itemName)
            itemPrices.append(itemPrice)
dict = {'itemNames': itemNames, 'itemCategory': categories, 'price': itemPrices, 'imageUrl': images}
df = pandas.DataFrame(dict)
df.to_csv('items.csv')
