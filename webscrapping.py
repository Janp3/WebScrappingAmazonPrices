from time import sleep

import openpyxl
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# creating excel documment
book = openpyxl.Workbook()
book.create_sheet('amazon_smartphones')
page = book['amazon_smartphones']
page.append(['Smartphone models', 'Price'])

path = 'https://www.amazon.com.br'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(path)

# searching smartphone
driver.find_element(By.ID, 'twotabsearchtextbox').send_keys('Smartphones')
sleep(.5)
driver.find_element(By.ID, 'nav-search-submit-button').click()
sleep(3)


main_element = driver.find_elements(
    By.XPATH,
    '//div[@class="a-section a-spacing-base"]'
)

# iterating through all the containers that has the title,
# price and others information
for element in main_element:
    try:
        title = element.find_element(
            By.XPATH,
            './/span[@class="a-size-base-plus a-color-base a-text-normal"]'
        ).text
        price = element.find_element(
            By.CLASS_NAME,
            'a-price-whole'
        ).text
        page.append([title, f"R$ {price}"])
    except NoSuchElementException:
        pass
book.save('Amazon prices.xlsx')
