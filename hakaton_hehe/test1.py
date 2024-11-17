import os
import json
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from yookassa import Configuration 
API_TOKEN = "8107372470:AAFlFdVfPCtpYGYqJXlxAm6-FwrF6co39Gk"
YOO_SHOP_ID = Configuration.account_id = 493387
YOO_API_KEY = Configuration.secret_key = 'test_gGQBvquPFCvw9c7vAS7Tx9L9Z2zZ1lpzPU8P9exG1W'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Добро пожаловать! Чтобы сделать тестовую оплату, введите сумму.")

@dp.message_handler()
async def process_payment(message: types.Message):
    try:
        # Пробуем преобразовать введенное сообщение в сумму
        amount = float(message.text)
            
        # Создаем заказ в ЮKassa
        payment_data = {
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://your.return.url/afterpayment"
            },
            "capture": True,
            "description": "Оплата за заказ"
        }

        # Запрос на оплату
        headers = {
            'Authorization': f'Bearer {YOO_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            f'https://api.yookassa.ru/v3/payments',
            json=payment_data,
            headers=headers,
            login="Мукминов Сабир Робертович",
            password="Kilokarik#@32"

        ) 

        if response.status_code == 201:
            response_data = response.json()
            payment_url = response_data['_embedded']['confirmation']['confirmation_url']
            await message.reply(f"Перейдите по ссылке для оплаты: {payment_url}")
        else:
            print(response)
            await message.reply("Ошибка при создании платежа. Попробуйте еще раз.")

    except ValueError:
        await message.reply("Пожалуйста, введите корректную сумму.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)