from bs4 import BeautifulSoup
from lxml import etree as et
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


product_keywords = ['Headset', 'Headset wire', 'Headset with mic', 'Headset wired', 'Headset wireless', 'Headset bluetooth',
                    'Headset wired with mic', 'Headset wireless with mic', 'Headset for mobile', 'Headset for laptop']
data_list = []
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.amazon.in")


def get_dom(base_url):
    driver.get(base_url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, 'html.parser')
    dom = et.HTML(str(product_soup))
    return dom


for keyword in product_keywords:
    search_box = driver.find_element(By.NAME, "field-keywords")
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    url = driver.current_url
    page_dom = get_dom(url)
    product_list = [keyword]
    sponsored_products = page_dom.xpath('//div[@class="a-row a-spacing-micro"]')
    for ele in sponsored_products:
        name = ele.xpath('./following::h2/a/span/text()')[0]
        product_list.append(name)
    data_list.append(product_list)


driver.quit()

with open('ppc_data3.csv', 'w', newline='', encoding='utf-8') as file:
    Writer = writer(file)
    Writer.writerow(['Keyword', 'Product 1', 'Product 2', 'Product 3', 'Product 4', 'Product 5', 'Product 6'])
    Writer.writerows(data_list)
