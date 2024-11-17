import logging
import keyboard as kb
from aiogram import Bot, Dispatcher, executor, types
import config as cfg
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
botApi = cfg.bot_api

bot = Bot(token=botApi)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help']) # можно @dp.message_handler() этот метод реагирует на любое сообщение 
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ ботяра")

@dp.message_handler(commands=['button']) # добавляет replybutton
async def process_start_command(message: types.Message):
    await message.reply("Привет, ты можешь нажать на кнопку", reply_markup=kb.greet_kb1)

@dp.message_handler(commands=['sikl']) 
async def check(message: types.Message): 
   await message.reply("hi! how are you", reply_markup=inli)

@dp.callback_query_handler(text=["button_1", "button_2"]) 
async def check_button(call: types.CallbackQuery): 
   if call.data == "button_1": 
       await call.message.answer("молодец ты нажал первую кнопку") 
   if call.data == "button_2": 
       await call.message.answer("молодец ты нажал вторую кнопку") 
   await call.answer()

if __name__ == '__main__':
    print("Бот Запущен")
    executor.start_polling(dp)
    