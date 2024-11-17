from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
button_1 = KeyboardButton('кнопка 1')# данная команда создаёт прототип кнопки с текстом
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_1) # этот метод добавляет прототипы в выборку
button_admin_create = KeyboardButton('Создать пользователя')
button_admin_change = KeyboardButton('Изменить данные пользователя')
button_admin_delete = KeyboardButton('Удалить пользователя')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_admin_create, button_admin_change, button_admin_delete)
contact = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True), KeyboardButton('Отправить свою локацию 🗺️', request_location=True))

# inline_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button_1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_1)
button1 = InlineKeyboardButton(text="Ссылка для оплаты:", url="https://www.google.com") 
keyboard_inline = InlineKeyboardMarkup().add(button1) 