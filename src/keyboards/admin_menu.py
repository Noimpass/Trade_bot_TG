from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb = [  
    [KeyboardButton(text="Редактировать товары")],
    [KeyboardButton(text="Меню пользователя")],
    [KeyboardButton(text="Меню бота")]
]

admin_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb = [
    [KeyboardButton(text="Добавить товар")],
    [KeyboardButton(text="Удалить товар")],
    [KeyboardButton(text="Изменить цену")],
    [KeyboardButton(text="Изменить количество")],
    [KeyboardButton(text="Назад")]
]

admin_menu_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb = [
        [KeyboardButton(text='Профиль'),
        KeyboardButton(text='Маркет')],
        [KeyboardButton(text='Поддержка'),
        KeyboardButton(text='Подробнее о сервисе')],
        [KeyboardButton(text='Управление ботом')]
]

start_admin_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
