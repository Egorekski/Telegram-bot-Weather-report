from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import asyncio
import webbrowser
import requests
import json
import datetime
import config

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

API = '2830c3b025d1ec68c26d2e56c78571db'


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(f"Hi, {message.from_user.full_name}! Welcome to our service. Please, choose one command.")


@dp.message(Command('website'))
async def website(message: Message):
    await message.answer("Website is open!")
    webbrowser.open('https://egorekski.github.io/resume/index.html')


@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer("This bot can show you the weather in your city."
                         "                                              "
                         "Any problems? Write to developer: @egorek_ski")


@dp.message(Command('current'))
async def current(message: Message):
    await message.answer("Please, write your city.")


@dp.message()
async def get_current_weather(message: Message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    code_to_pic = {
        "Clear": "Clear \U00002600",
        "Clouds": "Cloudy \U00002601",
        "Rain": "Rainy \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B",
    }

    try:

        data = json.loads(res.text)

        weather_description = data["weather"][0]["main"]
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        if weather_description in code_to_pic:
            wd = code_to_pic[weather_description]
        else:
            wd = "You're in crazy conditions!"

        if city == "moscow" or city == "москва":
            await message.reply(f"Date: {datetime.datetime.now().strftime('%Y/%m/%d')}\n"
                                f"Temperature: {round(data['main']['temp'])} C°\n"
                                f"Feels like: {round(data['main']['feels_like'])} C°\n"
                                f"Conditions: {wd}\n"
                                f"Wind: {round(data['wind']['speed'])} m/s\n"
                                f"Sunrise: {sunrise}\n"
                                f"Sunset: {sunset}\n")
        else:
            await message.reply(f"Date: {datetime.datetime.now().strftime('%Y/%m/%d')}\n"
                                f"Temperature: {round(data['main']['temp'])} C°\n"
                                f"Feels like: {round(data['main']['feels_like'])} C°\n"
                                f"Conditions: {wd}\n"
                                f"Wind: {round(data['wind']['speed'])} m/s\n")



    except TypeError:
        await message.answer("Something has gone wrong...")
        await message.reply("Check your data")
    except KeyError:
        await message.answer("Something has gone wrong...")
        await message.reply("Check your data")


async def main():
    try:
        await dp.start_polling(bot)
    except TypeError:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
