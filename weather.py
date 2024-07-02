import aiohttp
import asyncio
from config import weather_api_key


async def get_weather_forecast(city_name: str, api_key: str) -> dict | None:  # Функция парсит погоду по названию города
    # url геолокации
    geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(geocode_url) as geocode_response:
            if geocode_response.status == 200:  # Если запрос прошёл успешно
                data = await geocode_response.json()
                # Получаем высоту и широту локации
                lat = data[0]["lat"]
                lon = data[0]["lon"]

                # url прогноза погоды по геолокации
                weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                async with session.get(weather_url) as weather_response:  # Делаем запрос
                    if geocode_response.status == 200:  # Если запрос прошёл успешно
                        data = await weather_response.json()
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


async def main():
    city_name = "London"
    api_key = weather_api_key
    f = await get_weather_forecast(city_name, api_key)
    print(f"{f}")

if __name__ == "__main__":
    asyncio.run(main())
