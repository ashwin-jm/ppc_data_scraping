from bs4 import BeautifulSoup
from lxml import etree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import csv
import random
import time

# Keywords to search for on Amazon
product_keywords = [
    "Headset",
    "Headset wire",
    "Headset with mic",
    "Headset wired",
    "Headset wireless",
    "Headset bluetooth",
    "Headset wired with mic",
    "Headset wireless with mic",
    "Headset for mobile",
    "Headset for laptop",
]

# List to store the data for each keyword
data_list = []

# Start a Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Navigate to Amazon homepage
driver.get("https://www.amazon.in")


def get_dom(url):
    """
    Get the page source as a BeautifulSoup object, then convert to an lxml ET object.
    """
    driver.get(url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, "html.parser")
    dom = ET.HTML(str(product_soup))
    return dom


# Loop through each keyword
for keyword in product_keywords:
    # Enter the keyword into the search box
    print("Extracting data for keyword", keyword)
    search_box = driver.find_element(By.NAME, "field-keywords")
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    # Get the URL of the search results page
    url = driver.current_url

    # Get the DOM of the search results page
    page_dom = get_dom(url)

    # List to store the data for each keyword
    product_list = [keyword]

    # Get the sponsored products for this keyword
    sponsored_products = page_dom.xpath('//div[@class="a-row a-spacing-micro"]')

    # Loop through each sponsored product
    for ele in sponsored_products:
        name = ele.xpath("./following::h2/a/span/text()")[0]
        product_list.append(name)

    # Add the data for this keyword to the overall data list
    data_list.append(product_list)
    time.sleep(random.randint(3, 5))

# Quit the Chrome driver
driver.quit()

# Write the data to a CSV file
with open("ppc_data4.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Keyword",
            "Product 1",
            "Product 2",
            "Product 3",
            "Product 4",
            "Product 5",
            "Product 6",
        ]
    )
    writer.writerows(data_list)
