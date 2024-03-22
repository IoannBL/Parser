from telebot import TeleBot
from secret import TOKEN
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as undetected
import time
import re

bot = TeleBot(TOKEN)


class FlatFinderBot:
    def __init__(self, bot):
        self.user_states = {}
        self.bot = bot
        self.driver = None
        self.chat_id = None  # Добавляем переменную для хранения chat_id
    
    def start_bot(self):
        self.bot.polling()
    
    def start_message(self, message):
        self.bot.send_message(message.chat.id,
                              "Привет, я помогу подобрать тебе квартиру с нужными параметрами в нужной локации."
                              "Пожалуйста, введи название станции метро (например, 'Проспект мира'):")
        # Устанавливаем состояние "ожидание станции метро"
        self.user_states[message.chat.id] = 'awaiting_location'
        self.chat_id = message.chat.id  # Сохраняем chat_id
    
    # Остальные методы остаются без изменений
    def get_location(self, message):
        location = message.text
        self.bot.send_message(message.chat.id,
                              "Спасибо! Теперь введи максимальную стоимость квартиры (например, '65000'):")
        # Устанавливаем состояние "ожидание стоимости квартиры"
        self.user_states[message.chat.id] = 'awaiting_price'
        self.location = location
    def get_price(self, message):
        price = message.text
        self.bot.send_message(message.chat.id,
                              f"Спасибо! Обрабатываю данные... Ищу квартиры рядом с метро {self.location} не дороже {price} рублей")
        # Вызываем функцию парсинга с указанными параметрами
        self.parse_flats(int(price), self.location)
    def parse_flats(self, max_price, location):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        service = Service(ChromeDriverManager().install())
        self.driver = undetected.Chrome(service=service)
        
        http = "https://www.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/"
        self.driver.get(http)
        time.sleep(1)
        
        while True:
            flats = self.driver.find_elements(By.CLASS_NAME, "_93444fe79c--container--kZeLu._93444fe79c--link--DqDOy")
            for flat in flats:
                href = flat.find_element(By.CLASS_NAME, "_93444fe79c--link--VtWj6").get_attribute("href")
                desc = flat.find_element(By.CLASS_NAME, "_93444fe79c--link--VtWj6").text
                loc = flat.find_element(By.CLASS_NAME, "_93444fe79c--labels--L8WyJ").text
                price = flat.find_element(By.CLASS_NAME, "_93444fe79c--container--aWzpE").text
                price_desc = flat.find_element(By.CSS_SELECTOR, '[data-mark="PriceInfo"]').text
                digits = re.sub(r'\D', '', price)
                if int(digits) <= max_price and location in loc:
                    self.bot.send_message(self.chat_id,
                                          f"{href}\n{desc}\n{loc}\n{price}\n{price_desc}\n")  # Используем chat_id для отправки сообщения
            
            try:
                element = self.driver.find_element(By.XPATH, '//*[@id="frontend-serp"]/div/div[7]/div[2]/button[2]')
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                next_button = self.driver.find_element(By.XPATH,
                                                       '//nav[@data-name="Pagination"]/a[contains(span, "Дальше")]')
                next_button.click()
                time.sleep(2)
            except NoSuchElementException:
                break
        
        self.driver.quit()


flat_finder_bot = FlatFinderBot(bot)


@bot.message_handler(commands=['start'])
def start_message(message):
    flat_finder_bot.start_message(message)


@bot.message_handler(func=lambda message: flat_finder_bot.user_states.get(message.chat.id) == 'awaiting_location')
def get_location(message):
    flat_finder_bot.get_location(message)


@bot.message_handler(func=lambda message: flat_finder_bot.user_states.get(message.chat.id) == 'awaiting_price')
def get_price(message):
    flat_finder_bot.get_price(message)





if __name__ == "__main__":
    flat_finder_bot.start_bot()