import requests


def get_weather_forecast(city_name: str, api_key: str):  # Функция парсит погоду по названию города
    # url геолокации
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}"
    geocode_response = requests.get(geocode_url)
    if geocode_response.status_code == 200:  # Если запрос прошёл успешно
        data = geocode_response.json()
        # Получаем высоту и широту локации
        lat = data[0]["lat"]
        lon = data[0]["lon"]

        # url прогноза погоды по геолокации
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        weather_response = requests.get(weather_url)  # Делаем запрос

        if weather_response.status_code == 200:  # Если запрос прошёл успешно
            data = weather_response.json()
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
    else:
        return None
