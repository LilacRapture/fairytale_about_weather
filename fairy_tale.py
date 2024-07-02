import aiohttp
import asyncio

from weather_async import get_weather_forecast
from config import weather_api_key, gigachat_api_url, gigachat_token, yandex_api_url, yandex_token, yandex_project_id
# Для работы понадобятся:
# weather_api_key - токен OpenWeatherMap API
# gigachat_api_url - url для gigachat, например "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
# gigachat_token - токен для работы с gigachat, формируется с помощью токена авторизации, нужно обновлять
# yandex_api_url - url для yandex-gpt, например "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
# yandex_token - токен сервисного аккаунта в yandex облаке с правами ai.languageModels.user
# yandex_project_id - id каталога в облаке


# Функция получает на вход url модели нейросети, токен для api (должен быть сгенерирован) и параметры для запроса
async def get_fairy_tale_from_gigachat(api_url, api_key, genre, city, weather, max_length):
    prompt = (f"Придумай сказку в жанре {genre} про погоду на завтра {weather} в городе {city}. "
              f"Длина сказки не больше {max_length} символов.")

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": prompt  # Запрос
            }
        ],
        "temperature": 0.8,  # Точность(0)/случайность(1) генерации
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": max_length,  # Максимальное количество символов в ответе
    }

    async with aiohttp.ClientSession() as session:
        start_time = asyncio.get_event_loop().time()
        async with session.post(api_url, headers=headers, json=data) as response:
            end_time = asyncio.get_event_loop().time()
            response_time = end_time - start_time
            data = await response.json()
            tale = data['choices'][0]['message']['content']
            return tale, response_time


async def get_fairy_tale_from_yandex_gpt(api_url, api_key, project_id, genre, city, weather, max_length):
    prompt = (f"Придумай сказку в жанре {genre} про погоду на завтра {weather} в городе {city}. "
              f"Длина сказки не больше {max_length} символов.")

    headers = {
        'Authorization': f"API-KEY {api_key}",  # Токен
        'x-folder-id': project_id  # id каталога в облаке
    }

    data = {
        "modelUri": f"gpt://{project_id}/yandexgpt-lite",  # Указывается модель и id каталога
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": max_length
        },
        "messages": [
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        start_time = asyncio.get_event_loop().time()
        async with session.post(api_url, headers=headers, json=data) as response:
            end_time = asyncio.get_event_loop().time()
            response_time = end_time - start_time
            data = await response.json()
            tale = data['result']['alternatives'][0]['message']['text']
            return tale, response_time


async def main():
    # Запрос входных параметров
    requested_genre = input("Введите жанр: ")
    requested_city = input("Введите город: ")
    parsed_forecast = await get_weather_forecast(requested_city, weather_api_key)  # Парсим погоду в желаемом месте
    requested_max_length = int(input("Длина сказки в символах: "))

    # Делаем запрос к нейросети в параллельном режиме
    results = await asyncio.gather(
        get_fairy_tale_from_yandex_gpt(yandex_api_url, yandex_token, yandex_project_id, requested_genre, requested_city,
                                       parsed_forecast, requested_max_length),
        get_fairy_tale_from_gigachat(gigachat_api_url, gigachat_token, requested_genre, requested_city, parsed_forecast,
                                     requested_max_length)
    )
    # Собираем результаты в словарь
    yandex_response_text, yandex_response_time = results[0]
    gigachat_response_text, gigachat_response_time = results[1]

    # Записываем время и ответ в файл
    with open('yandex_response.txt', 'w', encoding='utf-8') as f:
        f.write(f"Время работы yandex-gpt: {yandex_response_time} секунд\n")
        f.write(yandex_response_text)
    print(f"Yandex-gpt время работы: {yandex_response_time} секунд, файл с ответом: gigachat_response.txt.")

    with open('gigachat_response.txt', 'w', encoding='utf-8') as f:
        f.write(f"Время работы gigachat: {gigachat_response_time} секунд\n")
        f.write(gigachat_response_text)
    print(f"Gigachat время работы: {gigachat_response_time} секунд, файл с ответом: gigachat_response.txt.")


asyncio.run(main())
