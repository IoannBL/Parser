from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as undetected
from selenium.webdriver.common.by import By
import time
import re
from telebot import TeleBot
from secret import TOKEN

bot = TeleBot(TOKEN)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
service = Service(ChromeDriverManager().install())
driver = undetected.Chrome(service=service)

# Открытие страницы
http = "https://www.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/"
driver.get(http)
time.sleep(1)


# Функция для получения данных с текущей страницы
def getting_data(driver):
    flats = driver.find_elements(By.CLASS_NAME, "_93444fe79c--container--kZeLu._93444fe79c--link--DqDOy")
    data = []
    for flat in flats:
        href = flat.find_element(By.CLASS_NAME, "_93444fe79c--link--VtWj6").get_attribute("href")
        desc = flat.find_element(By.CLASS_NAME, "_93444fe79c--link--VtWj6").text
        loc = flat.find_element(By.CLASS_NAME, "_93444fe79c--labels--L8WyJ").text
        price = flat.find_element(By.CLASS_NAME, "_93444fe79c--container--aWzpE").text
        price_desc = flat.find_element(By.CSS_SELECTOR, '[data-mark="PriceInfo"]').text
        data.append((href, desc, loc, price, price_desc, " "))
    return data


# Условия фильтрации
p = 300000
l = "Тестовская"

while True:
    # Получаем данные с текущей страницы
    parsed_data = getting_data(driver)
    
    # Выводим данные с текущей страницы
    for d in parsed_data:
        digits = re.sub(r'\D', '', d[3])
        if int(digits) <= p and l in d[2]:
            print(d[0])
            print(d[1])
            print(d[2])
            print(d[3])
            print(d[4])
            print(d[5])

    try:
        element = driver.find_element(By.XPATH, '//*[@id="frontend-serp"]/div/div[7]/div[2]/button[2]')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        next_button = driver.find_element(By.XPATH, '//nav[@data-name="Pagination"]/a[contains(span, "Дальше")]')
        next_button.click()
        time.sleep(2)  # Подождать, чтобы страница полностью загрузилась
    except NoSuchElementException:
        break

driver.quit()


