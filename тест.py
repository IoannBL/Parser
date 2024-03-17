import re

text = """
Отличное предложение!
2-комн. квартира, 38 м², 26/33 этаж
Москва, САО, р-н Головинский, м. Водный стадион, Кронштадтский бульвар, 8к1
70 000 ₽/мес.
От года, комм. платежи включены (без счётчиков), комиссия 60%, залог 70 000 ₽
"""

rooms = re.search(r"(\d+)\-комн\.", text).group(1)
area = re.search(r"(\d+(\.\d+)?) м²", text).group(1)
floor_info = re.search(r"(\d+)/(\d+) этаж", text)
floor_current = floor_info.group(1)
floor_total = floor_info.group(2)
district_metro = re.search(r"р-н (.+?), м. (.+?),", text)
district = district_metro.group(1)
metro_station = district_metro.group(2)
address = re.search(r"м. .+, (.+)", text).group(1)
price = re.search(r"(\d+(?:\s+\d+)*(?:\.\d+)?) ₽/мес", text).group(1)
terms = re.search(r"От года, (.+)", text).group(1)

print("Количество комнат:", rooms)
print("Площадь:", area)
print("Этаж:", floor_current, "/", floor_total)
print("Район:", district)
print("Станция метро:", metro_station)
print("Адрес:", address)
print("Стоимость аренды:", price)
print("Условия аренды:", terms)