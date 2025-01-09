import requests
from telegram import Update
from telegram.ext import Application, CommandHandler
import logging
import os

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для получения погоды с Open-Meteo для Москвы
def get_weather_moscow():
    latitude = 55.7522
    longitude = 37.6156
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,snowfall,pressure_msl,wind_speed_10m'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            current_data = data['hourly']
            temperature = current_data['temperature_2m'][0]
            humidity = current_data['relative_humidity_2m'][0]
            apparent_temp = current_data['apparent_temperature'][0]
            precipitation = current_data['precipitation'][0]
            snowfall = current_data['snowfall'][0]
            pressure = current_data['pressure_msl'][0]
            wind_speed = current_data['wind_speed_10m'][0]
            
            pressure_mmHg = pressure / 1.33322
            
            weather_info = (
                f"<b>Температура (Москва):</b> {temperature}°C\n"
                f"<b>Ощущаемая температура:</b> {apparent_temp}°C\n"
                f"<b>Влажность:</b> {humidity}%\n"
                f"<b>Осадки:</b> {precipitation} мм\n"
                f"<b>Снегопад:</b> {snowfall} мм\n"
                f"<b>Давление:</b> {pressure_mmHg:.2f} мм рт. ст.\n"
                f"<b>Скорость ветра:</b> {wind_speed} м/с"
            )
            return weather_info
        except KeyError:
            return "Ошибка: неверная структура данных в ответе от API."
    else:
        return f"Ошибка при запросе к API: {response.status_code}. Ответ: {response.text}"

# Функция для получения погоды с Open-Meteo для Брянска
def get_weather_bryansk():
    latitude = 53.15
    longitude = 34.22
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,snowfall,pressure_msl,wind_speed_10m'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            current_data = data['hourly']
            temperature = current_data['temperature_2m'][0]
            humidity = current_data['relative_humidity_2m'][0]
            apparent_temp = current_data['apparent_temperature'][0]
            precipitation = current_data['precipitation'][0]
            snowfall = current_data['snowfall'][0]
            pressure = current_data['pressure_msl'][0]
            wind_speed = current_data['wind_speed_10m'][0]
            
            pressure_mmHg = pressure / 1.33322
            
            weather_info = (
                f"<b>Температура (Брянск):</b> {temperature}°C\n"
                f"<b>Ощущаемая температура:</b> {apparent_temp}°C\n"
                f"<b>Влажность:</b> {humidity}%\n"
                f"<b>Осадки:</b> {precipitation} мм\n"
                f"<b>Снегопад:</b> {snowfall} мм\n"
                f"<b>Давление:</b> {pressure_mmHg:.2f} мм рт. ст.\n"
                f"<b>Скорость ветра:</b> {wind_speed} м/с"
            )
            return weather_info
        except KeyError:
            return "Ошибка: неверная структура данных в ответе от API."
    else:
        return f"Ошибка при запросе к API: {response.status_code}. Ответ: {response.text}"

# Функция для получения погоды с Open-Meteo для Чадыр-Лунга
def get_weather_chadyr_lunga():
    latitude = 46.0318
    longitude = 28.49
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,snowfall,pressure_msl,wind_speed_10m'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            current_data = data['hourly']
            temperature = current_data['temperature_2m'][0]
            humidity = current_data['relative_humidity_2m'][0]
            apparent_temp = current_data['apparent_temperature'][0]
            precipitation = current_data['precipitation'][0]
            snowfall = current_data['snowfall'][0]
            pressure = current_data['pressure_msl'][0]
            wind_speed = current_data['wind_speed_10m'][0]
            
            pressure_mmHg = pressure / 1.33322
            
            weather_info = (
                f"<b>Температура (Чадыр-Лунга):</b> {temperature}°C\n"
                f"<b>Ощущаемая температура:</b> {apparent_temp}°C\n"
                f"<b>Влажность:</b> {humidity}%\n"
                f"<b>Осадки:</b> {precipitation} мм\n"
                f"<b>Снегопад:</b> {snowfall} мм\n"
                f"<b>Давление:</b> {pressure_mmHg:.2f} мм рт. ст.\n"
                f"<b>Скорость ветра:</b> {wind_speed} м/с"
            )
            return weather_info
        except KeyError:
            return "Ошибка: неверная структура данных в ответе от API."
    else:
        return f"Ошибка при запросе к API: {response.status_code}. Ответ: {response.text}"

# Функция для обработки команды /weather
async def weather(update: Update, context):
    weather_info_moscow = get_weather_moscow()
    weather_info_bryansk = get_weather_bryansk()
    weather_info_chadyr_lunga = get_weather_chadyr_lunga()
    
    # Формируем красивое сообщение с использованием HTML
    message = (
        f"<b>🌞 Погода в Москве:</b>\n{weather_info_moscow}\n\n"
        f"<b>🌧 Погода в Брянске:</b>\n{weather_info_bryansk}\n\n"
        f"<b>🌬 Погода в Чадыр-Лунга:</b>\n{weather_info_chadyr_lunga}\n\n"
        "<i>Информация предоставлена Димой</i>"
    )
    
    # Получаем chat_id из запроса
    chat_id = update.message.chat_id
    
    try:
        # Отправляем сообщение в чат, откуда была вызвана команда
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения в чат {chat_id}: {e}")

# Основная функция для запуска бота
async def main():
    application = Application.builder().token(
        os.environ.get("TOKEN")
    ).build()
    application.add_handler(CommandHandler("weather", weather))  # Команда /weather
    # Запускаем бота без polling, так как запросы будут только по команде
    await application.run_polling(poll_interval=20)  # Увеличьте время интервала если хотите.

if __name__ == "__main__":
    try:
        application = Application.builder().token("7315724244:AAEH6Wzr_2yI9f5nj5ZLRdiGqgJ3sb7yobM").build()
        application.add_handler(CommandHandler("weather", weather))
        application.run_polling(poll_interval=60)  # Будет опрашивать каждую минуту
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
