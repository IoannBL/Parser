import asyncio
from telebot.async_telebot import AsyncTeleBot
from secret import TOKEN
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as undetected
import time
import re
import os
# current_directory = os.path.dirname(os.path.abspath(__file__))

bot = AsyncTeleBot(TOKEN)

class FlatFinderBot:
    def __init__(self, bot):
        self.user_states = {}
        self.bot = bot
        self.driver = None
        self.chat_id = None
        self.parsing = True
    async def start_bot(self):
        await self.bot.polling()
    
    async def stop_parsing(self,message):
        self.parsing = False
        await self.bot.send_message(message.chat.id,"Поиск остановлен")
        
    async def help_pars(self,message):
        await self.bot.send_message(message.chat.id,
                                    "Список команд:"
                                    "'/start '- начало поиска, "
                                    "'/stop '- остановка поиска ")
        
    async def start_message(self, message):
        await self.bot.send_message(message.chat.id,
                              "Привет, я помогу подобрать тебе квартиру с нужными параметрами в нужной локации."
                              "Пожалуйста, введи название станции метро с большой буквы (например, 'Тестовская'):")
        self.user_states[message.chat.id] = 'location'
        self.chat_id = message.chat.id
    
    async def get_location(self, message):
        location = message.text
        with open('verification_file.txt', 'r', encoding='utf-8') as file:
            metro_stations = file.readlines()
            metro_stations = [station.strip() for station in metro_stations]
        
        if location.lower() not in [station.strip().lower() for station in metro_stations]:
            await self.bot.send_message(message.chat.id,
                                        "Введенная станция метро не найдена. Пожалуйста, введите корректное название станции метро:")
            return
        
        await self.bot.send_message(message.chat.id,
                                    "Спасибо! Теперь введите максимальную стоимость квартиры (например, '65000'):")
        self.user_states[message.chat.id] = 'price'
        self.location = location
    async def get_price(self, message):
        price = message.text
        if not price.isdigit():
            await self.bot.send_message(message.chat.id,
                                        "Используйте при вводе стоимости квартиры только цифры. Попробуйте снова.")
            return
        await self.bot.send_message(message.chat.id,
                              f"Спасибо! Обрабатываю данные... Ищу квартиры рядом с метро {self.location} не дороже {price} рублей")
        self.user_states[message.chat.id] = 'stop_pars'
        await self.parse_flats(int(price), self.location)
    async def parse_flats(self, max_price, location):
        options = Options()
        options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        
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
                if int(digits) <= max_price and (location.lower() in loc.lower() or location == "1"):
                    await self.bot.send_message(self.chat_id,
                                          f"{href}\n{desc}\n{loc}\n{price}\n{price_desc}\n")
            if not self.parsing:
                break
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
async def start_message(message):
    await flat_finder_bot.start_message(message)

@bot.message_handler(func=lambda message: flat_finder_bot.user_states.get(message.chat.id) == 'location')
async def get_location(message):
    await flat_finder_bot.get_location(message)

@bot.message_handler(func=lambda message: flat_finder_bot.user_states.get(message.chat.id) == 'price')
async def get_price(message):
    await flat_finder_bot.get_price(message)
    
@bot.message_handler(commands=['stop'],func=lambda message: flat_finder_bot.user_states.get(message.chat.id) == 'stop_pars')
async def stop_parsing(message):
    await flat_finder_bot.stop_parsing(message)
    
@bot.message_handler(commands=['help'])
async def stop_parsing(message):
    await flat_finder_bot.help_pars(message)

if __name__ == "__main__":
    asyncio.run(flat_finder_bot.start_bot())