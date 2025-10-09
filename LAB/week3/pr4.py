# import os
# os.system("pip install selenium")
  
# import os
# os.system("pip install beautifulsoup4")
 
 
# from selenium import webdriver  
# from bs4 import BeautifulSoup  
# import pandas as pd #install chrom webdriver  
# #webdriver can be downloaded from  
# #https://sites.google.com/chromium.org/driver/downloads/  
# driver = webdriver.Chrome()  
  
# products=[] #List to store name of the product prices=[] #List to store 
# prices =[]
# ratings=[] #List to store rating of the product 
# driver.get("https://www.flipkart.com/search?q=gming%20laptop&otracker=search &otracker1=search&marketplace=FLIPKART&as-show=on&as=off")  
  
# content = driver.page_source  
# soup = BeautifulSoup(content)   
# # print(soup)  
# for a in soup.findAll('div',attrs={'class':'tUxRFH'}): 
#      print (a)  
#      name=a.find('a', attrs={'class':'KzDlHZ'})     
#      price=a.find('div',attrs={'class':'Nx9bqj _4b5DiR'})   
#      rating=a.find('div',attrs={'class':'XQDdHH'})      
#      products.append(name.text)      
#      prices.append(price.text) 
#      ratings.append(rating.text)  
  
# df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})   
# df.to_csv('products.csv', index=False, encoding='utf-8')


import os
os.system("pip install selenium")
os.system("pip install beautifulsoup4")

from selenium import webdriver  
from bs4 import BeautifulSoup  
import pandas as pd

# Initialize Chrome driver
driver = webdriver.Chrome()  

products = []  # List to store name of the product
prices = []    # List to store prices
ratings = []   # List to store rating of the product

driver.get("https://www.flipkart.com/search?q=gaming%20laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")  

content = driver.page_source  
soup = BeautifulSoup(content, 'html.parser')  # Specify parser to avoid warning

# Find all product containers
for a in soup.findAll('div', attrs={'class':['tUxRFH', '_1AtVbE', 'col-12-12']}): 
    # Extract product name
    name_element = a.find('div', attrs={'class':['KzDlHZ', '_4rR01T']})
    name = name_element.text if name_element else "N/A"
    
    # Extract price
    price_element = a.find('div', attrs={'class':['Nx9bqj', '_4b5DiR', '_30jeq3', '_1_WHN1']})
    price = price_element.text if price_element else "N/A"
    
    # Extract rating
    rating_element = a.find('div', attrs={'class':['XQDdHH', '_3LWZlK']})
    rating = rating_element.text if rating_element else "N/A"
    
    # Only append if we have at least the product name
    if name != "N/A":
        products.append(name)
        prices.append(price)
        ratings.append(rating)

# Close the driver
driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame({
    'Product Name': products,
    'Price': prices, 
    'Rating': ratings
})   

df.to_csv('products.csv', index=False, encoding='utf-8')
print("Data successfully saved to products.csv")
print(f"Scraped {len(products)} products")