import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from weather import get_weather_forecast
from config import weather_api_key, gigachat_api_url, gigachat_token, yandex_api_url, yandex_token, yandex_project_id
# Для работы понадобятся:
# weather_api_key - токен OpenWeatherMap API
# gigachat_api_url - url для gigachat, например "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
# gigachat_token - токен для работы с gigachat, формируется с помощью токена авторизации, нужно обновлять
# yandex_api_url - url для yandex-gpt, например "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
# yandex_token - токен сервисного аккаунта в yandex облаке с правами ai.languageModels.user
# yandex_project_id - id каталога в облаке


# Функция получает на вход url модели нейросети, токен для api (должен быть сгенерирован) и параметры для запроса
def get_fairy_tale_from_gigachat(api_url, api_key, genre, city, weather, max_length):
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

    start_time = time.time()
    # verify=False нужен если не установлены сертификаты НУЦ Минцифры
    response = requests.post(api_url, headers=headers, json=data, verify=False)
    end_time = time.time()

    response_time = end_time - start_time  # Считаем время работы
    response_text = response.json()['choices'][0]['message']['content']  # Достаём ответ сети

    return response_text, response_time


def get_fairy_tale_from_yandex_gpt(api_url, api_key, project_id, genre, city, weather, max_length):
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

    start_time = time.time()
    response = requests.post(api_url, headers=headers, json=data)
    end_time = time.time()

    response_time = end_time - start_time
    response_text = response.json()['result']['alternatives'][0]['message']['text']  # Достаём ответ сети

    return response_text, response_time


# Запрос входных параметров
requested_genre = input("Введите жанр: ")
requested_city = input("Введите город: ")
parsed_forecast = get_weather_forecast(requested_city, weather_api_key)  # Парсим погоду в желаемом месте
requested_max_length = int(input("Длина сказки в символах: "))


# Делаем запрос к нейросети в параллельном режиме
with ThreadPoolExecutor() as executor:
    future_yandex = executor.submit(get_fairy_tale_from_yandex_gpt, yandex_api_url, yandex_token, yandex_project_id,
                                                              requested_genre, requested_city, parsed_forecast,
                                                              requested_max_length)
    future_gigachat = executor.submit(get_fairy_tale_from_gigachat, gigachat_api_url, gigachat_token, requested_genre,
                                                                requested_city, parsed_forecast, requested_max_length)

    # Собираем результаты в словарь
    results = {}
    for future in as_completed([future_yandex, future_gigachat]):
        if future == future_yandex:
            results['yandex'] = future.result()
        else:
            results['gigachat'] = future.result()


# Записываем время и ответ в файл
with open('yandex_response.txt', 'w', encoding='utf-8') as f:
    f.write(f"Время работы yandex-gpt: {results['yandex'][1]} seconds\n")
    f.write(results['yandex'][0])
print(f"Yandex-gpt время работы: {results['yandex'][1]}, файл с ответом: gigachat_response.txt.")

with open('gigachat_response.txt', 'w', encoding='utf-8') as f:
    f.write(f"Время работы gigachat: {results['gigachat'][1]} seconds\n")
    f.write(results['gigachat'][0])
print(f"Gigachat время работы: {results['gigachat'][1]}, файл с ответом: gigachat_response.txt.")
