import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://dienmaythiennamhoa.vn/'
r = requests.get(url)
soup = bs(r.content, 'html.parser')

#print(soup.prettify())

product_list = []
products = soup.find_all('div', attrs={'class':'card-cate'})

for product in products:
    #print(product.prettify())
    name = product.find('h3').text.strip()
    price =  product.find('p', attrs={'class':'sale-price product-sale-price'}).text.strip()
    product_list.append([name, price])

# with open('ketqua.csv','w', encoding='utf-8') as file:
#     file.write(', ten sp, gia,\n')
#     for i, product in enumerate(products):
#         print(product.prettify())
#         name = product.find('h3').text.strip()
#         price =  product.find('p', attrs={'class':'sale-price product-sale-price'}).text.strip()
#         product_list.append([name, price])
#         file.write(str(i)+','+name+','+price+',\n')

dataFrame = pd.DataFrame(product_list, columns=['Ten San Pham','Gia'])
print(dataFrame)
dataFrame.to_csv('result.csv')