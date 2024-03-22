import main
from telebot.async_telebot import AsyncTeleBot
from secret import TOKEN
import asyncio

bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(message.chat.id, "Привет, я помогу подобрать тебе квартиру с нужными параметрами в нужной локации.\n\n"
                                      "Пожалуйста, введи название станции метро (например, 'Проспект мира'):")

@bot.message_handler(func=lambda message: True)
async def get_location(message):
    global location
    location = message.text
    await bot.send_message(message.chat.id, "Спасибо! Теперь введи максимальную стоимость квартиры (например, '65000'):")

@bot.message_handler(func=lambda message: True)
async def get_price(message):
    global price
    price = message.text
    await bot.send_message(message.chat.id, "Спасибо! Обрабатываю данные...")

pars(price,location)
    # Здесь можно вызвать ваш парсер, передавая в него переменные location и price
    # Получить результат парсинга

    # В данном примере просто отправляем обратно полученные данные
    bot.send_message(message.chat.id, "Данные успешно получены! Мы нашли подходящие варианты квартир.")
    # Пример отправки данных пользователям
    # for flat in parsed_data:
    #     bot.send_message(message.chat.id, f"Ссылка: {flat[0]}\nОписание: {flat[1]}\nЛокация: {flat[2]}\nСтоимость: {flat[3]}\nОписание цены: {flat[4]}\n")

if __name__ == "__main__":
    asyncio.run(bot.polling())