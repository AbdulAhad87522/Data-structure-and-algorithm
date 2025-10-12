from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configure Chrome options for speed
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Initialize driver with options
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.flipkart.com/search?q=gaming%20laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    
    # Wait for products to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_37K3-p"))
    )
    
    # Small delay to ensure all content loads
    time.sleep(2)
    
    products = []
    prices = []
    ratings = []
    
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    
    # More specific container selection
    product_containers = soup.find_all('div', class_='_37K3-p')
    
    print(f"Found {len(product_containers)} products")
    
    for container in product_containers:
        try:
            # Product name with error handling
            name_elem = container.find('a', class_='s1Q9rs')
            name = name_elem.text.strip() if name_elem else "N/A"
            
            # Price with error handling
            price_elem = container.find('div', class_='_30jeq3')
            price = price_elem.text.strip() if price_elem else "N/A"
            
            # Rating with error handling
            rating_elem = container.find('div', class_='_3LWZlK')
            rating = rating_elem.text.strip() if rating_elem else "No Rating"
            
            # Only add if we have at least the product name
            if name != "N/A":
                products.append(name)
                prices.append(price)
                ratings.append(rating)
                
        except Exception as e:
            print(f"Error parsing product: {e}")
            continue
    
    # Create DataFrame
    df = pd.DataFrame({
        'Product Name': products,
        'Price': prices, 
        'Rating': ratings
    })
    
    df.to_csv('products.csv', index=False, encoding='utf-8')
    print(f"Successfully saved {len(products)} products to products.csv")

except Exception as e:
    print(f"Error during scraping: {e}")

finally:
    driver.quit()