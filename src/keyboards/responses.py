import logging

from dispatcher import dp, bot
from aiogram import types, html, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, LinkPreviewOptions
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards.menu import *
from keyboards.state import *
from db.dataspace import ManageUsers
from db.models import Users


options_1 = LinkPreviewOptions(is_disabled=True)

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!", reply_markup = start_kb)
    if ManageUsers().get_user_by_id(message.from_user.id) == None:
        user_data = Users(
            user_id = message.from_user.id,
            username = message.from_user.username,
            balance = 0,
            deals = 0,
            bonus = 0,
            trade_link = None
        )
        ManageUsers().add_user(user_data)

@dp.message(F.text.lower() == "профиль")
async def send_profile_info(message: Message) -> None:
    user_data = ManageUsers().get_user_by_id(message.from_user.id)
    await message.answer(f"Пользователь: {user_data.username}\nID профиля: {user_data.user_id}\nКоличество сделок: {user_data.deals}\nБаланс: {user_data.balance}\nTrade link: <a href = '{user_data.trade_link}'>NEED FIX</a>", reply_markup=profile_kb, link_preview_options=options_1)

# NEED TO MAKE IT PRETTY
@dp.callback_query(F.data == "change_link")
async def change_link(callback:CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.change_link)
    await callback.message.answer(f"Отправляйте Trade link:", reply_markup=change_link_kb)

# need to add functionality
@dp.message(Form.change_link, F.text.startswith("https://steamcommunity.com/tradeoffer/new/?partner="))
async def link_changed(message: Message, state: FSMContext) -> None:
    if message.text != None:
        await state.clear()
        await message.answer(f"Trade link успешно изменён")
        await send_profile_info(message)
        ManageUsers().change_trade_link(message.from_user.id, message.text)
    else:
        pass
    
@dp.callback_query(F.data == "отмена")
async def cancel_handler(callback:CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    logging.info(f"Cancelling state {current_state}")
    user_data = ManageUsers().get_user_by_id(callback.from_user.id)
    await state.clear()
    await bot.send_message(f"username: {user_data.username}\nID профиля: {user_data.user_id}\nКоличество сделок: {user_data.deals}\nБаланс: {user_data.balance}\nTrade link: {user_data.trade_link}", reply_markup=profile_kb, link_preview_options=options_1)

@dp.message(F.text.lower() == "маркет")
async def send_market_info(message: Message) -> None:
    await message.answer(f"Выберите категорию", reply_markup=market_kb)


@dp.message(F.text.lower() == "подробнее о сервисе")
async def send_about_info(message: Message) -> None:
    message.answer(f"Подробнее о сервисе")

@dp.message(F.text.lower() == "поддержка")
async def send_support_info(message: Message) -> None:
    message.answer(f"Поддержка")


@dp.callback_query(F.data == "TF2")
async def send_TF2_info(message: Message) -> None:
    await message.answer(f"товар")

@dp.callback_query(F.data == "CS2")
async def send_TF2_info(message: Message) -> None:
    await message.answer(f"товар")