import undetected_chromedriver as uc
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os


names = []
prices = []
minimunorders = []
total_sold = []
suppliers = []
olds = []
suppliers_type =[]
suppliers_location =[]
suppliers_name =[]
driver = uc.Chrome()
try:
    for i in range(20,40):
        url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&from=pcHomeContent&has4Tab=true&keywords=tshirt&originKeywords=tshirt&tab=all&page={i}"
        # responce = requests.get(url)
        driver.get(url)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fy26-product-card-content"))
        )
        # time.sleep(4)
        
        
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
                sold = product.find('div', class_= 'searchx-sold-order')
                total = sold.text.strip() if sold else'N/A'
                supplier_div = product.find('div', class_='searchx-product-area supplier-area-layout')
                if supplier_div:
                    # Find all individual span elements within supplier div
                    supplier_spans = supplier_div.find_all('span')
                    
                    # Extract different supplier attributes
                    supplier = supplier_div.text.strip()
                    supplier_name = supplier_spans[0].text.strip() if len(supplier_spans) > 0 else 'N/A'
                    supplier_type = supplier_spans[1].text.strip() if len(supplier_spans) > 1 else 'N/A'
                    supplier_location = supplier_spans[2].text.strip() if len(supplier_spans) > 2 else 'N/A'
                else:
                    supplier_name = 'N/A'
                    supplier_type = 'N/A'
                    supplier_location = 'N/A'
                old = product.find('div', class_= 'searchx-product-e-popper__trigger')
                final_old = old.text.strip() if old else 'N/A'
                names.append(final_name)
                prices.append(final_price)
                minimunorders.append(final_minimum)
                total_sold.append(total)
                suppliers.append(supplier_name)
                suppliers_type.append(supplier_type)
                suppliers_location.append(supplier_location)
                suppliers_name.append(supplier)
                # olds.append(final_old)
                print(f"total of {len(names)} scrapedd in {i} iterations")
                
            except Exception as e:
                print(f"Error scraping products {e}")
                continue
        
         
    df = pd.DataFrame({
        "Names" : names,
        "Price" : prices,
        "Minimum Orders" : minimunorders,
        "Total Sold" : total_sold,
        "Supplier Name" : suppliers_name,   
        "Supplier's Experience" : suppliers,
        "Supplier Country" : suppliers_type,
        "Supplier Rating" : suppliers_location
        # "Years" : olds
        })
        
    df.to_csv("machinery40-60.csv", index = False, encoding="UTF-8")
    # if os.path.exists("s-20.csv"):
    #     print(f"CSV file created successfully! Total products scraped: {len(names)}")
    #     print(f"File location: {os.path.abspath('s-20.csv')}")
    # else:
    #     print("CSV file was not created!")
    
    print(f"Total products scraped are {len(names)}")

finally:
     driver.quit

