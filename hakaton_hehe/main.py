import logging
import keyboard as kb
from aiogram import Bot, Dispatcher, executor, types
from yookassa import Configuration
Configuration.account_id = 493387
Configuration.secret_key = 'test_gGQBvquPFCvw9c7vAS7Tx9L9Z2zZ1lpzPU8P9exG1W'

bot_api = "8107372470:AAFlFdVfPCtpYGYqJXlxAm6-FwrF6co39Gk"


bot = Bot(token=bot_api)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help']) # можно @dp.message_handler() этот метод реагирует на любое сообщение 
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ ботяра")

@dp.message_handler(commands=['button']) # добавляет replybutton
async def process_start_command(message: types.Message):
    await message.reply("Привет, ты можешь нажать на кнопку", reply_markup=kb.greet_kb1)

@dp.message_handler(commands=['sikl']) 
async def check(message: types.Message): 
   await message.reply("hi! how are you", reply_markup=kb.keyboard_inline)

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
    