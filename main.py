import requests
from telegram import Update
from telegram.ext import Application, CommandHandler
import logging
import os

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для получения погоды с Open-Meteo для нескольких точек
def get_weather():
    # Координаты для 3 точек: Москва, Брянск, Чадыр-Лунга
    latitudes = [46.0617, 53.2521, 55.7522]
    longitudes = [28.8308, 34.3717, 37.6156]
    locations = ['Чадыр-Лунга', 'Брянск', 'Москва']

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitudes[0]},{latitudes[1]},{latitudes[2]}&longitude={longitudes[0]},{longitudes[1]},{longitudes[2]}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,snowfall,wind_speed_10m,wind_direction_10m&timezone=auto&forecast_days=1'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            weather_info = ""
            for i in range(3):
                location = locations[i]
                current_data = data['current']
                
                # Получаем данные для каждой точки
                temperature = current_data['temperature_2m'][i]
                humidity = current_data['relative_humidity_2m'][i]
                apparent_temp = current_data['apparent_temperature'][i]
                precipitation = current_data['precipitation'][i]
                rain = current_data['rain'][i]
                snowfall = current_data['snowfall'][i]
                wind_speed = current_data['wind_speed_10m'][i]
                wind_direction = current_data['wind_direction_10m'][i]
                
                weather_info += (
                    f"<b>🌍 Погода в {location}:</b>\n"
                    f"<b>Температура:</b> {temperature}°C\n"
                    f"<b>Ощущаемая температура:</b> {apparent_temp}°C\n"
                    f"<b>Влажность:</b> {humidity}%\n"
                    f"<b>Осадки:</b> {precipitation} мм\n"
                    f"<b>Дождь:</b> {rain} мм\n"
                    f"<b>Снегопад:</b> {snowfall} мм\n"
                    f"<b>Скорость ветра:</b> {wind_speed} м/с\n"
                    f"<b>Направление ветра:</b> {wind_direction}°\n\n"
                )
            }
            return weather_info
        except KeyError:
            return "Ошибка: неверная структура данных в ответе от API."
    else:
        return f"Ошибка при запросе к API: {response.status_code}. Ответ: {response.text}"

# Функция для обработки команды /weather
async def weather(update: Update, context):
    weather_info = get_weather()  # Получаем погоду для всех трех точек
    
    # Формируем красивое сообщение с использованием HTML
    message = weather_info + "<i>Информация предоставлена Open-Meteo</i>"
    
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
        application = Application.builder().token("YOUR_BOT_TOKEN").build()
        application.add_handler(CommandHandler("weather", weather))
        application.run_polling(poll_interval=60)  # Будет опрашивать каждую минуту
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
