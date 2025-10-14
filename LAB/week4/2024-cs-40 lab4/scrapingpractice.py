

import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


names = []
prices = []
minimunorders = []
driver = uc.Chrome()
try:
    for i in range(1,2):
        url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&categoryId=66010502&has4Tab=true&keywords=Tattoo+Ink&originKeywords=Tattoo+Ink&productId=60775230598&tab=all&&page={i}&spm=a2700.galleryofferlist.pagination.0"
        # responce = requests.get(url)
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fy26-product-card-content"))
        )
        time.sleep(4)
        
        
        soup = bs(driver.page_source, 'html.parser')
        products = soup.find_all('div', class_= "fy26-product-card-content")
        
        for product in products:
            try:
                name = product.find('h2', class_='searchx-product-e-title')
                final_name = name.text.strip() if name else'N/A'
                price = product.find('div', class_="searchx-product-price-price-main")
                final_price = price.text.strip() if price else'N/A'
                minimun = product.find('div', class_="searchx-moq")
                final_minimum = minimun.text.strip() if minimun else'N/A'
                names.append(final_name)
                prices.append(final_price)
                minimunorders.append(final_minimum)
                print(f"total of {len(names)} scrapedd in {i} iterations")
                
            except Exception as e:
                print(f"Error scraping products {e}")
                continue
        
        
    df = pd.DataFrame({
        "Names" : names,
        "Price" : prices,
        "Minimum Orders" : minimunorders
        })
        
        
    df.to_csv("products.csv", index = "false", encoding="UTF-8")
    print(f"Total products scraped are {len(names)}")

finally:
     driver.quit



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup as bs
# import pandas as pd
# import time

# # Setup Chrome driver
# driver = webdriver.Chrome()  # Make sure chromedriver is in PATH
# driver.maximize_window()

# try:
#     url = "https://www.alibaba.com/trade/search?spm=a27aq.cp_66.5538637320.7.15a13bbc1On6JS&categoryId=66010502&SearchText=Tattoo+Ink&indexArea=product_en&fsb=y&tab=all&has4Tab=true&productId=60775230598"
#     driver.get(url)
    
#     # Wait for products to load
#     WebDriverWait(driver, 15).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "fy26-product-card-content"))
#     )
    
#     # Additional wait to ensure all content loads
#     time.sleep(3)
    
#     # Get page source after JavaScript execution
#     soup = bs(driver.page_source, 'html.parser')
#     products = soup.find_all('div', class_="fy26-product-card-content")
    
#     print(f"Found {len(products)} product containers")
    
#     names = []
#     prices = []
#     minimumorders = []
    
#     for product in products:
#         try:
#             # Use find() instead of find_all() for single elements
#             name_elem = product.find('h2', class_='searchx-product-e-title')
#             price_elem = product.find('div', class_="searchx-product-price-price-main")
#             minimum_elem = product.find('div', class_="searchx-moq")
            
#             # Check if elements exist before accessing .text
#             final_name = name_elem.text.strip() if name_elem else "N/A"
#             final_price = price_elem.text.strip() if price_elem else "N/A"
#             final_minimum = minimum_elem.text.strip() if minimum_elem else "N/A"
            
#             names.append(final_name)
#             prices.append(final_price)
#             minimumorders.append(final_minimum)
            
#             print(f"Scraped: {final_name} | {final_price} | {final_minimum}")
            
#         except Exception as e:
#             print(f"Error scraping product: {e}")
#             continue
    
#     # Create DataFrame
#     df = pd.DataFrame({
#         "Names": names,
#         "Price": prices,
#         "Minimum Orders": minimumorders
#     })
    
#     df.to_csv("products.csv", index=False, encoding="UTF-8")
#     print(f"Total products scraped: {len(names)}")
    
#     # Show first few rows
#     if len(df) > 0:
#         print("\nFirst 3 products:")
#         print(df.head(3))

# finally:
#     driver.quit()