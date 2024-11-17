import json, logging, sqlite3, asyncio
import config as cfg
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from yookassa import Configuration, Payment
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from admin import role_admin
from user import role_user

# Настройка логирования
logging.basicConfig(level=logging.INFO)
new_my_role = "admin"
# Инициализация бота и диспетчера
API_TOKEN = cfg.bot_api  # Ваш токен Telegram бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Настройка YooKassa
Configuration.account_id = cfg.shop_id  # Ваш shop_id
Configuration.secret_key = cfg.secret_key  # Ваш secret_key

# Переменные для отслеживания состояния
is_authorized = False
awaiting_amount = False  # Флаг для отслеживания ожидания суммы
amount = None  # Переменная для хранения введенной суммы

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    global is_authorized
    is_authorized = False  # Сбрасываем авторизацию при старте
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
    await message.reply("Привет! Для начала работы, нужно авторизоваться. :", reply_markup=markup_request)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contacts(msg: types.Message):
    global is_authorized
    if msg.chat.id == msg.contact.user_id:
        result_contact = msg.contact.phone_number
        try:
            with sqlite3.connect('database/heton.db', check_same_thread=False) as conn:
                cur = conn.cursor()
                cur.execute("SELECT phone_number FROM user WHERE phone_number = ?", (result_contact,))
                a = cur.fetchall()
                if a:
                    is_authorized = True  # Устанавливаем авторизацию
                    cur.execute(f"SELECT role FROM user WHERE phone_number = {result_contact}")
                    my_role = cur.fetchall()
                    new_my_role = my_role[0][0]
                    await bot.send_message(msg.from_user.id, text="Вы авторизовались. Для оплаты введите /buy")
                else:
                    await bot.send_message(msg.from_user.id, text="Вас нет в базе данных. Попробуйте снова.")
        except Exception as e:
            logging.error(f"Ошибка при доступе к базе данных: {e}")
            await bot.send_message(msg.from_user.id, text="Произошла ошибка. Попробуйте снова.")
    else:
        await bot.send_message(msg.from_user.id, text="Вы отправили не свою контактную информацию")

@dp.message_handler(commands=['buy'])
async def cmd_buy(message: types.Message):
    if(is_authorized):
        global awaiting_amount, amount
        awaiting_amount = True  # Устанавливаем флаг ожидания суммы
        await message.answer("Введите сумму для покупки:")
    else:
        await message.answer("Вы не авторизованы. Пожалуйста, авторизуйтесь с помощью команды /start")

@dp.message_handler(lambda message: message.text.isdigit())
async def process_amount(message: types.Message):
    global awaiting_amount, amount
    if awaiting_amount:  # Проверяем, ожидаем ли мы сумму
        amount = int(message.text)  # Сохраняем введенную сумму
        awaiting_amount = False  # Сбрасываем флаг после ввода суммы
        await message.answer(f"Вы выбрали сумму: {amount} RUB. Подтвердите покупку командой /confirm.")
    else:
        await message.answer("Пожалуйста, сначала введите команду /buy для начала процесса покупки.")

@dp.message_handler(commands=['confirm'])
async def cmd_confirm(message: types.Message):
    global amount
    if amount is None:  # Проверяем, была ли введена сумма
        await message.answer("Сначала введите сумму с помощью команды /buy.")
        return

    # Здесь ваша логика для подтверждения и транзакции
    description = "Покупка товара."  # Описание платежа
    payment_response = payment(amount, description)

    if payment_response:
        # Отправляем ссылку для оплаты
        keyboard_inline = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Ссылка для оплаты:", url=f"{payment_response['confirmation']['confirmation_url']}"))
        await message.reply("Ссылка для оплаты:", reply_markup=keyboard_inline)

        # Проверяем статус платежа
        await check_payment(payment_response['id'], message.from_user.id)
    else:
        await message.answer("Произошла ошибка при создании платежа.")

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def check_payment(payment_id, user_id):
    while True:
        payment = json.loads((Payment.find_one(payment_id)).json())
        if payment['status'] == 'succeeded':
            # Форматируем сообщение о платеже
            payment_info = (
                f"Платеж успешен! Спасибо за покупку.\n"
                f"Сумма: {payment['amount']['value']} {payment['amount']['currency']}\n"
                f"ID платежа: {payment['id']}\n"
                f"Статус: {payment['status']}\n"
                f"Дата создания: {payment['created_at']}\n"
                f"Метод оплаты: {payment['payment_method']['title']}\n"
            )
            await bot.send_message(user_id, text=payment_info)  # Отправляем структурированное сообщение
            break
        elif payment['status'] == 'canceled':
            await bot.send_message(user_id, text="Платеж отменен.")
            break
        await asyncio.sleep(3)  # Проверяем статус каждые 3 секунды

def payment(value, description):
    try:
        payment = Payment.create({
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"  # Укажите тип платежа
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://your_redirect_url.com"  # Укажите ваш URL редиректа
            },
            "capture": True,
            "description": description
        })
        return json.loads(payment.json())
    except Exception as e:
        logging.error(f"Ошибка при создании платежа: {e}")
        return None

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    # Проверка роли
    if new_my_role == 'admin':
        role_admin(dp, bot)  
    else:
        role_user(dp, bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
