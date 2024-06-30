import requests


def get_weather_forecast(city_name: str, api_key: str):  # Функция парсит погоду по названию города
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"  # Формируем url
    response = requests.get(complete_url)  # Делаем запрос

    if response.status_code == 200:  # Если запрос прошёл успешно
        data = response.json()  # Разбираем данные из json
        main = data['main']
        weather = data['weather'][0]
        forecast = {
            'city': data['name'],
            'temperature': main['temp'],
            'pressure': main['pressure'],
            'humidity': main['humidity'],
            'description': weather['description']
        }  # Формируем готовые данные о погоде
        return forecast
    else:
        return None
