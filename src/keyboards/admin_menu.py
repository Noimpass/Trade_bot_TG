from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb = [  
    [KeyboardButton(text="Редактировать товары")],
    [KeyboardButton(text="Меню пользователя")]
]

admin_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb = [
    [KeyboardButton(text="Добавить товар"),
    KeyboardButton(text="Удалить товар")],
    [KeyboardButton(text="Изменить цену"),
    KeyboardButton(text="Изменить количество")],
    [KeyboardButton(text="Назад")]
]

product_menu_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

