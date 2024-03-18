from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as undetected
from selenium.webdriver.common.by import By
import time
import re
service = Service(ChromeDriverManager().install())
driver = undetected.Chrome(service=service)



http = "https://www.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/"
driver.get(http)


time.sleep(1)
flats = driver.find_elements(By.CLASS_NAME, "_93444fe79c--container--kZeLu._93444fe79c--link--DqDOy")

# for flat in flats:
#     text = flat.text
#     print(text)

# print(len(flats))
# data = [(i.find_element(By.CSS_SELECTOR, "_93444fe79c--row--kEHOK"),
#          ""
#          ) for i in flats]
# for d in data:
#     print(d[0])
#     print(d[1])
#
# driver.quit()

data = []
for flat in flats:
    href = flat.find_element(By.CLASS_NAME, "_93444fe79c--link--VtWj6").get_attribute("href")
    desc = flat.find_element(By.CLASS_NAME, "_93444fe79c--link--VtWj6").text
    loc = flat.find_element(By.CLASS_NAME, "_93444fe79c--labels--L8WyJ").text
    price = flat.find_element(By.CLASS_NAME, "_93444fe79c--container--aWzpE").text
    price_desc = flat.find_element(By.CSS_SELECTOR, '[data-mark="PriceInfo"]').text
    data.append((desc, loc, price, price_desc, " "))
# Вывод данных

p = 300000
l = "Смоленская"
for d in data:
    digits = re.sub(r'\D', '', d[2])
    if int(digits) >= p and l in d[1]:
        print(href)
        print(d[0])
        print(d[1])
        print(d[2])
        print(d[3])
        print(d[4])
driver.quit()