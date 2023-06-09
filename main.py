from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_BOT, qiwi_token, phone
import logging
import asyncio
from SimpleQIWI import *


bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=MemoryStorage())
loop = asyncio.new_event_loop()
logging.basicConfig(level=logging.INFO)

api = QApi(token=qiwi_token, phone=phone)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    bt1 = KeyboardButton('Баланс')
    bt2 = KeyboardButton('История платежей')
    markup.add(bt1, bt2)
    await bot.send_message(message.chat.id,
                           text=f"Добро пожаловать, {message.from_user.first_name}!\nТы попал в QIWI Bank, но в телеграмме!\nОн сделан для тех, у кого нет времени зайти в QIWI, и кому удобнее смотреть всё в тг.\nВыберете что вас интересует", reply_markup=markup)


@dp.message_handler(text='Баланс')
async def bln(message: types.Message):
    await bot.send_message(message.chat.id,
                           text=f'Ваш баланс: {(api.balance[0])} рублей')


@dp.message_handler(text='История платежей')
async def history(message: types.Message):

    file = open('payments.txt', 'w')
    file.write(f"{(api.payments)}")
    file.close()


    await bot.send_document(message.chat.id, document=open('payments.txt', 'rb'))











if __name__ == '__main__':
    executor.start_polling(dp ,loop=loop)





