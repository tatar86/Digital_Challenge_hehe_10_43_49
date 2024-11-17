import asyncio
import logging

from aiogram import Bot, types
from aiogram import executor
from aiogram import Dispatcher
from aiogram.types.message import ContentType
import config as cfg

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot_token = cfg.bot_api
provider_secret_token = cfg.secret_key
provider_token_ = cfg.provider_token

loop = asyncio.get_event_loop()

bot = Bot(bot_token, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, loop=loop)

PRICE = types.LabeledPrice(label='гипер турбо мяч', amount=6000)

MESSAGES = {
    'successful_payment': '✅ Спасибо за оплату! Сумма: {} {}\nПереходите в бота: https://t.me/your_bot_username'
}

@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    try:
        await bot.send_invoice(
            message.chat.id,
            title="Жёсткий турбо гипер мяч",
            description="такого вы нигде не найдёте",
            provider_token=provider_token_,
            currency='RUB',  # Убедитесь, что валюта указана правильно
            photo_url="https://img.razrisyika.ru/kart/19/72628-dop-12.jpg",
            photo_height=512,
            photo_width=512,
            photo_size=512,
            is_flexible=False,
            prices=[PRICE],
            start_parameter='time-machine-example',
            payload='some-invoice-payload-for-our-internal-use'
        )
    except Exception as e:
        logging.error(f"Ошибка при создании счёта: {e}")

@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print("shtjuckbdgftn")
    try:
        print("ok") 
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Ошибка")
        print()
    except Exception as e:
        print(f"Ошибк: {e}")

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    # Убедитесь, что вы используете правильные атрибуты
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            message.successful_payment.total_amount // 100,
            message.successful_payment.currency
        )
    )

if __name__ == '__main__':
    print("Бот Запущен")
    executor.start_polling(dp, skip_updates=True)