from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as undetected
from selenium.webdriver.common.by import By
import time

service = Service(ChromeDriverManager().install())
driver = undetected.Chrome(service=service)



http = "https://www.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/"
driver.get(http)


time.sleep(1)
"поиск элементов по тегу"
flats = driver.find_elements(By.CLASS_NAME, "div._93444fe79c--content--lXy9G")

print(len(flats))
data = [(i.find_element(By.CLASS_NAME, "div._93444fe79c--link--BwwJO").find_element(By.TAG_NAME, "a").get_attribute("title"),
         ""
         ) for i in flats]
for d in data:
    print(d[0])
    print(d[1])


time.sleep(10000)