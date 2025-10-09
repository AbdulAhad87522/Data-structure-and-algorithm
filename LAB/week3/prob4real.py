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
teachers = []

driver.get("https://eduko.spikotech.com/Course")  

content = driver.page_source  
soup = BeautifulSoup(content, 'html.parser')  # Specify parser to avoid warning

# Find all product containers
for a in soup.findAll('div', attrs={'class':['col-md-4 mb-4 d-flex align-items-stretch', '_1AtVbE', 'col-12-12']}): 
    # Extract product name
    name_element = a.find('div', attrs={'class':['card-body text-center', '_4rR01T']})
    name = name_element.h4.text if name_element else "N/A"
    
    # Extract price
    description_element = a.find('div', attrs={'class':['card-body text-center', '_4b5DiR', '_30jeq3', '_1_WHN1']})
    description = description_element.text if description_element else "N/A"
    # extract teacher name
    teacher_element = a.find('div', attrs={'class':['card-body text-center', '_4b5DiR', '_30jeq3', '_1_WHN1']})
    teacher = teacher_element.h7.text if teacher_element else "N/A"
    

    
    # Only append if we have at least the product name
    if name != "N/A":
        products.append(name)
        prices.append(description)
        teachers.append(teacher)

# Close the driver
driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame({
    'Course Name': products,
    'description': prices, 
    'Teacher Name' : teachers,
})   

df.to_csv('eduko.csv', index=False, encoding='utf-8')
print("Data successfully saved to eduko.csv")
print(f"Scraped {len(products)} products")