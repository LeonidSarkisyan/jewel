import requests

from src.config import WEATHER_API_KEY, WEATHER_URL
from src.weather.russian_cities import search_cities_from_file


def processing_data(json_data: dict):
    data = dict()
    data["temp"] = json_data["main"]["temp"]
    data["temp_feels_like"] = json_data["main"]["feels_like"]
    data["type"] = json_data["weather"][0]["description"].capitalize()
    data["humidity"] = json_data["main"]["humidity"]
    data["pressure"] = json_data["main"]["pressure"]
    return data


def search_cities(search_string: str):
    cities = search_cities_from_file(search_string)
    return cities


class OpenWeatherService:

    query_params = f"&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

    def get_weather_by_coords(self, lat: float, lon: float):
        query = self.url + f"?lat={lat}&lon={lon}" + self.query_params
        response = requests.get(query)
        return self.valid_response(response, InvalidCoords(f"Координаты lat={lat} lon={lon} были введены некорректно."))

    def get_weather_by_city(self, city_name: str):
        query = self.url + f"?q={city_name},RU" + self.query_params
        response = requests.get(query)
        return self.valid_response(response, CityNotFound(f"Город {city_name} не был найден в базе."))

    @staticmethod
    def valid_response(response, error: Exception):
        if response.status_code == 200:
            weather_data = processing_data(response.json())
            return weather_data
        else:
            raise error


class CityNotFound(Exception):
    pass


class InvalidCoords(Exception):
    pass


weather_service = OpenWeatherService(WEATHER_URL, WEATHER_API_KEY)

print(weather_service.get_weather_by_city("Пудож"))
