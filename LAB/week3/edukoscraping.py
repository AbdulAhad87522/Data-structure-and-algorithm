# import os
# os.system("pip install selenium")
# os.system("pip install beautifulsoup4")

# from selenium import webdriver  
# from bs4 import BeautifulSoup  
# import pandas as pd

# # Initialize Chrome driver
# driver = webdriver.Chrome()  

# products = []  # List to store name of the product
# prices = []    # List to store prices
# teachers = []

# driver.get("https://eduko.spikotech.com/Course")  

# content = driver.page_source  
# soup = BeautifulSoup(content, 'html.parser')  # Specify parser to avoid warning

# # Find all product containers
# for a in soup.findAll('div', attrs={'class':['col-md-4 mb-4 d-flex align-items-stretch']}): 
#     # Extract product name
#     name_element = a.find('div', attrs={'class':['card-body text-center', '_4rR01T']})
#     name = name_element.h4.text if name_element else "N/A"
    
#     # Extract price
#     description_element = a.find('div', attrs={'class':['card-body text-center']})
#     description = description_element.text if description_element else "N/A"
#     # extract teacher name
#     teacher_element = a.find('div', attrs={'class':['card-body text-center']})
#     teacher = teacher_element.h7.text if teacher_element else "N/A"
    

    
#     # Only append if we have at least the product name
#     if name != "N/A":
#         products.append(name)
#         prices.append(description)
#         teachers.append(teacher)

# # Close the driver
# driver.quit()

# # Create DataFrame and save to CSV
# df = pd.DataFrame({
#     'Course Name': products,
#     'description': prices, 
#     'Teacher Name' : teachers,
# })   

# df.to_csv('eduko.csv', index=False, encoding='utf-8')
# print("Data successfully saved to eduko.csv")
# print(f"Scraped {len(products)} products")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# service = Service("C:/Users/User/Desktop/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome()

driver.get("https://eduko.spikotech.com/Course")
time.sleep(7)

cards = driver.find_elements(By.CLASS_NAME, "card-body")
print("Total courses:", len(cards))

codes = []
titles = []
descs = []
clo1 = []
clo2 = []
clo3 = []
clo4 = []
tb1 = []
tb2 = []
instructors = []
semesters = []

for i in range(len(cards)):
    try:
        print(f"\nScraping course {i+1} ...")
        card = cards[i]

        title_tag = card.find_element(By.CLASS_NAME, "card-title")
        title = title_tag.text.strip()

        h7_tags = card.find_elements(By.TAG_NAME, "h7")
        instructor = h7_tags[0].text.strip() if len(h7_tags) > 0 else "None"
        semester = h7_tags[1].text.strip() if len(h7_tags) > 1 else "None"

        link_tag = card.find_element(By.TAG_NAME, "a")
        href = link_tag.get_attribute("href")

        driver.execute_script("window.open(arguments[0]);", href)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        code_tag = soup.find("div", {"id": "CourseCode"})
        course_code = code_tag.text.strip() if code_tag else "None"

        desc_tag = soup.find("p", {"id": "CourseDescription"})
        desc = desc_tag.text.strip() if desc_tag else "No Description"

        clo_list = soup.find("ul", {"id": "CourseClos"})
        clo_items = [li.text.strip() for li in clo_list.find_all("li")] if clo_list else []
        c1 = clo_items[0] if len(clo_items) > 0 else "None"
        c2 = clo_items[1] if len(clo_items) > 1 else "None"
        c3 = clo_items[2] if len(clo_items) > 2 else "None"
        c4 = clo_items[3] if len(clo_items) > 3 else "None"

        book_list = soup.find("ul", {"id": "CourseBooks"})
        book_items = [li.text.strip() for li in book_list.find_all("li")] if book_list else []
        t1 = book_items[0] if len(book_items) > 0 else "None"
        t2 = book_items[1] if len(book_items) > 1 else "None"

        codes.append(course_code)
        titles.append(title)
        descs.append(desc)
        clo1.append(c1)
        clo2.append(c2)
        clo3.append(c3)
        clo4.append(c4)
        tb1.append(t1)
        tb2.append(t2)
        instructors.append(instructor)
        semesters.append(semester)

        print(f"Done: {title}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)

    except Exception as e:
        print(f"Error course {i+1} pe:", e)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)
        continue

df = pd.DataFrame({
    "CourseCode": codes,
    "Title": titles,
    "Description": descs,
    "CLO1": clo1,
    "CLO2": clo2,
    "CLO3": clo3,
    "CLO4": clo4,
    "TextBook1": tb1,
    "TextBook2": tb2,
    "Instructor": instructors,
    "Semester": semesters
})

df.to_csv("EdukoCourses.csv", index=False, encoding="utf-8")
print("\nData saved in : EdukoCourses.csv")

driver.quit()