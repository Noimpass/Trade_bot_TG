from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


kb = [
        [KeyboardButton(text='Профиль'),
        KeyboardButton(text='Маркет')],
        [KeyboardButton(text='Поддержка'),
        KeyboardButton(text='Подробнее о сервисе')] 
]

start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

kb = [
        [InlineKeyboardButton(text="Изменить ссылку", callback_data="change_link"),
        InlineKeyboardButton(text="бонусы за продажу", callback_data="bonus")],
        [InlineKeyboardButton(text="Вывод средств", callback_data="withdraw"),
        InlineKeyboardButton(text="Пополнить баланс", callback_data="deposit")]
]

profile_kb = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [
        [InlineKeyboardButton(text="Team Fortress 2", callback_data="TF2")],
        [InlineKeyboardButton(text="CS2", callback_data="CS2")]
]

market_kb = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [
    [InlineKeyboardButton(text="Купить", callback_data="pay")],
    [InlineKeyboardButton(text="Продать", callback_data="sell")]
]

pay_kb = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [
    [InlineKeyboardButton(text="Купить", callback_data="yes")],
    [InlineKeyboardButton(text="Отмена", callback_data="отмена")]
]

buy_kb = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [
    [InlineKeyboardButton(text="Подтвердить", callback_data="confirmation")],
    [InlineKeyboardButton(text="Отмена", callback_data="отмена")]
]

confirmation_kb = InlineKeyboardMarkup(inline_keyboard=kb)

kb = [
    [InlineKeyboardButton(text="Как узнать свой Trade link", url="https://steamcommunity.com/id/me/tradeoffers/privacy#trade_offer_access_url")],
    [InlineKeyboardButton(text="Отмена", callback_data="отмена")]
]

change_link_kb = InlineKeyboardMarkup(inline_keyboard=kb) 
