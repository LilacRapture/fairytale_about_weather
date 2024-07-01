# fairytale_about_weather
# Getting Neural Network to Write Fairytale About Weather in Specific Place

## Overview

This project leverages AI models and APIs to generate a fairytale based on the weather conditions of a specific location. It utilizes several APIs and AI services:
- **OpenWeatherMap** for fetching weather forecasts based on geographical coordinates.
- **YandexGPT** for crafting the fairytale content.
- **Gigachat** for crafting the fairytale content.

## Prerequisites

To get started with this project, ensure you have:
- An internet connection.
- Python installed on your system.
- The `requests` package installed.
- Access to the following accounts and tokens:
  - [OpenWeatherMap](https://openweathermap.org/api): Sign up for an API key at https://home.openweathermap.org/users/sign_up.
  - [Yandex Cloud](https://yandex.cloud/ru/docs/foundation-models/concepts/yandexgpt/): Create an account and obtain a folder ID and service account token with the “ai.languageModels.user” role.
  - [Sber](https://developers.sber.ru/docs/ru/gigachat/api/overview): Obtain an access token for the Gigachat API.


## Usage

1. Clone the repository to your local machine.
2. Set up environment variables for your API keys and tokens.
3. Run fairy_tale.py to fetch weather data and generate the fairytales.
4. Check created yandex_response.txt and gigachat_response.txt to see the results and time taken by both AIs.

