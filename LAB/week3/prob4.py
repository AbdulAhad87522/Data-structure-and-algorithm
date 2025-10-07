# from selenium import webdriver  
# from bs4 import BeautifulSoup  
# import pandas as pd #install chrom webdriver  
# #webdriver can be downloaded from  
# #https://sites.google.com/chromium.org/driver/downloads/  
# driver = webdriver.Chrome(executable_path='G:\Program Files\Anaconda3\chromdriver\chromedriver.exe')  
  
# products=[] #List to store name of the product prices=[] #List to store 
# price of the product ratings=[] #List to store rating of the product 
# driver.get("https://www.flipkart.com/search?q=gming%20laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")  
  
# content = driver.page_source  
# soup = BeautifulSoup(content)  
# # print(soup)  
# for a in soup.findAll('div',attrs={'class':'_37K3-p'}): 
#      print (a)  
#      name=a.find('a', attrs={'class':'s1Q9rs'})     
#      price=a.find('div',attrs={'class':'_30jeq3'})   
#      rating=a.find('div',attrs={'class':'_3LWZlK'})      
#      products.append(name.text)      
#      prices.append(price.text) 
#      ratings.append(rating.text)  
  
# df = pd.DataFrame({'Product Name':products,'Price':prices,'Rating':ratings})   
# df.to_csv('products.csv', index=False, encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize WebDriver (modern approach)
driver = webdriver.Chrome()

products = []
prices = []
ratings = []

try:
    driver.get("https://www.flipkart.com/search?q=gaming%20laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    
    # Wait for page to load
    time.sleep(3)
    
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
    # Inspect the current page to find correct selectors
    # These are example selectors - you need to update them
    for a in soup.findAll('div', attrs={'class': '_2kHMtA'}):  # Update this class
        try:
            name_elem = a.find('div', attrs={'class': '_4rR01T'})  # Update this
            price_elem = a.find('div', attrs={'class': '_30jeq3'})
            rating_elem = a.find('div', attrs={'class': '_3LWZlK'})
            
            if name_elem and price_elem:
                products.append(name_elem.text)
                prices.append(price_elem.text)
                ratings.append(rating_elem.text if rating_elem else 'No Rating')
                
        except Exception as e:
            print(f"Error parsing product: {e}")
            continue

finally:
    driver.quit()

# Create DataFrame only if we have data
if products:
    df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Rating': ratings})
    df.to_csv('products.csv', index=False, encoding='utf-8')
    print(f"Saved {len(products)} products to products.csv")
else:
    print("No products found. Check your selectors.")