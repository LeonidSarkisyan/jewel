from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.keyboards.weather import get_main_weather_menu_keyboard, get_location_keyboard, get_cities_list_keyboard
from src.utils.messages import (
    MAIN_WEATHER_MESSAGE, ASK_GEOLOCATION_MESSAGE, get_message_about_weather, GET_GEOLOCATION_MESSAGE,
    INCORRECT_LOCATION_MESSAGE, CHOOSE_CITY_MESSAGE, get_city_weather_message, ASK_SEARCH_CITY_MESSAGE,
    INCORRECT_SEARCH_MESSAGE
)
from src.weather.service import weather_service


router = Router()


@router.callback_query(F.data == "weather")
async def weather_menu(call: CallbackQuery):
    await call.message.edit_text(MAIN_WEATHER_MESSAGE, reply_markup=get_main_weather_menu_keyboard())


class WeatherLocationState(StatesGroup):
    get_location = State()


@router.callback_query(F.data == "ask_weather")
async def weather_location(call: CallbackQuery, state: FSMContext):
    await call.message.answer(ASK_GEOLOCATION_MESSAGE, reply_markup=get_location_keyboard())
    await state.set_state(WeatherLocationState.get_location)


@router.message(WeatherLocationState.get_location)
async def get_location(message: Message, state: FSMContext):
    if message.location:
        await message.answer(GET_GEOLOCATION_MESSAGE)
        weather = weather_service.get_weather_by_coords(message.location.latitude, message.location.longitude)
        await message.answer(get_message_about_weather(weather), reply_markup=None)
        await state.clear()
    else:
        await message.answer(INCORRECT_LOCATION_MESSAGE)


@router.callback_query(F.data == "city_weather")
async def send_city_list(call: CallbackQuery):
    await call.message.edit_text(CHOOSE_CITY_MESSAGE, reply_markup=get_cities_list_keyboard())


@router.callback_query(F.data.startswith("weather_city__"))
async def get_city_weather(call: CallbackQuery):
    city = call.data.split("__")[-1]
    await call.message.answer(get_city_weather_message(city))
    weather = weather_service.get_weather_by_city(city)
    await call.message.answer(get_message_about_weather(weather), reply_markup=None)
    await call.answer()


class CitySearchStates(StatesGroup):
    get_search = State()


@router.callback_query(F.data == "search_city")
async def ask_search_string_city(call: CallbackQuery, state: FSMContext):
    await call.message.answer(ASK_SEARCH_CITY_MESSAGE)
    await state.set_state(CitySearchStates.get_search)
    await call.answer()


@router.message(CitySearchStates.get_search)
async def send_list_city_by_search(message: Message, state: FSMContext):
    if message.text:
        await message.answer(CHOOSE_CITY_MESSAGE, reply_markup=get_cities_list_keyboard(message.text))
        await state.clear()
    else:
        await message.answer(INCORRECT_SEARCH_MESSAGE)
