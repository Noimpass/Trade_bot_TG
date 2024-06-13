import logging

from dispatcher import dp, bot
from aiogram import types, html, F
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards.menu import *
from keyboards.state import *
from db.dataspace import ManageUsers, ManageProducts, ManageAdmins
from db.models import Users
from request.request import *
from config import settings


options_1 = LinkPreviewOptions(is_disabled=True)

market_TF2 = []

market_CS2 = []

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
            trade_link = None,
            steam_link = None
        )
        ManageUsers().add_user(user_data)

@dp.message(F.text.lower() == "профиль")
async def send_profile_info(message: Message) -> None:
    user_data = ManageUsers().get_user_by_id(message.from_user.id)
    await message.answer(f"Пользователь: {user_data.username}\nID профиля: {user_data.user_id}\nКоличество сделок: {user_data.deals}\nБаланс: {user_data.balance}\nTrade link: <a href = '{user_data.steam_link}'>{user_data.steam_name}</a>", reply_markup=profile_kb, link_preview_options=options_1)


@dp.callback_query(F.data == "change_link")
async def change_link(callback:CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.change_link)
    await callback.message.answer(f"Отправляйте Trade link:", reply_markup=change_link_kb)

@dp.message(Form.change_link, F.text.startswith("https://steamcommunity.com/tradeoffer/new/?partner="))
async def link_changed(message: Message, state: FSMContext) -> None:
    response1 = Request().get_profile_id(message.text)
    try:
        if response1 != None:
            await state.clear()
            await message.answer(f"Trade link успешно изменён")
            ManageUsers().change_trade_link(message.from_user.id, message.text)
            response = Request().get_profile_name(response1)
            ManageUsers().change_steam_link(message.from_user.id, response[0])
            ManageUsers().change_steam_name(message.from_user.id, response[1])
            await send_profile_info(message)
        else:
            await message.answer(f"Не удалось изменить trade link")
    except:
        await message.answer(f"Не удалось изменить trade link")
    
@dp.callback_query(F.data == "отмена")
async def cancel_handler(callback:CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    logging.info(f"Cancelling state {current_state}")
    user_data = ManageUsers().get_user_by_id(callback.from_user.id)
    await state.clear()
    await bot.send_message(callback.from_user.id, f"Операция отменена", reply_markup=start_kb)
    #await bot.send_message(callback.from_user.id, f"Пользователь: {user_data.username}\nID профиля: {user_data.user_id}\nКоличество сделок: {user_data.deals}\nБаланс: {user_data.balance}\nTrade link: <a href = '{user_data.steam_link}'>{user_data.steam_name}</a>", reply_markup=profile_kb, link_preview_options=options_1)

@dp.callback_query(F.data == "deposit")
async def deposit_balance(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Deposit.deposit_amount)
    await bot.send_message(callback.from_user.id, f"Ввведите сумму пополнения баланса\nМинимальная сумма пополнения: 100 руб.")

@dp.message(Deposit.deposit_amount)
async def deposit_amount(message: Message, state: FSMContext) -> None:
    if int(message.text) >= int(100) and int(message.text) <= int(930000):
        await state.update_data({"deposit_amount": message.text})
        kb_builder = InlineKeyboardBuilder()
        kb_builder.add(InlineKeyboardButton(text="Подтвердить", callback_data="confirmation"))
        kb_builder.add(InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        await message.answer(f"Ваш хотите пополнить баланс на {message.text} руб.?", reply_markup=kb_builder.as_markup(resize_keyboard=True))
    else:
        await message.answer(f"Ведена некорректная сумма. Минимальная сумма пополнения: 100 руб.")


@dp.callback_query(F.data == "confirmation")
async def deposit_confirm(callback:CallbackQuery, state: FSMContext) -> None:
    state_data = await state.get_data()
    await bot.send_invoice(chat_id = callback.from_user.id,
                            title = "Пополнение баланса",
                            description = f"Пополнение баланса на {state_data['deposit_amount']} руб.",
                            payload = "test",
                            provider_token = settings.TEST_SHOP_TOKEN,
                            currency = "RUB",
                            start_parameter = "test",
                            prices = [LabeledPrice(label="Пополнение баланса", amount=int(state_data["deposit_amount"])*100)],
                            protect_content = True,
                            need_shipping_address=False)


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext) -> None:
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.clear()

@dp.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext) -> None:
    ManageUsers().change_balance(message.from_user.id, message.successful_payment.total_amount /100)
    user_data = ManageUsers().get_user_by_id(message.from_user.id)
    await message.answer(f"Пользователь: {user_data.username}\nID профиля: {user_data.user_id}\nКоличество сделок: {user_data.deals}\nБаланс: {user_data.balance}\nTrade link: <a href = '{user_data.steam_link}'>{user_data.steam_name}</a>", reply_markup=profile_kb, link_preview_options=options_1)
    await state.clear()

@dp.callback_query(F.data == "withdraw")
async def withdraw_balance(callback: CallbackQuery) -> None:
    await bot.send_message(callback.from_user.id, f"Для вывода средств на баланс, сввяжитесь с администратором.\nАдминистратор - @Noimf")

@dp.callback_query(F.data == "bonus")
async def send_bonus_info(callback: CallbackQuery) -> None:
    user_data = ManageUsers().get_user_by_id(callback.from_user.id)
    await bot.send_message(callback.from_user.id, f"Количество купленных и проданных товаров: {user_data.bonus}\n100 товаров = 0.2% скидка от суммы покупкии продажи\n250 товаров = 0.3% скидка от суммы покупкии продажи\n500 товаров = 0.4% скидка от суммы покупкии продажи")

@dp.message(F.text.lower() == "маркет")
async def send_market_info(message: Message) -> None:
    user_data = ManageUsers().get_user_by_id(message.from_user.id)
    if user_data.trade_link == None:
        await message.answer(f"Сначала заполните профиль")
    else:
        await message.answer(f"Выберите категорию", reply_markup=market_kb)


@dp.message(F.text.lower() == "подробнее о сервисе")
async def send_about_info(message: Message) -> None:
    await message.answer(
f"Приветствую, геймеры!
Ищете способ пополнить Steam в России?
Наш телеграмм-бот - ваш идеальный помощник!
                                                 
Как начать:
Введите свой Trade link в профиле бота. 
Пополните кошелёк в боте
Выберите нужный товаров, который вас интересует.
Оформите заказ и подтвердите покупку.
Согласитесь на Trade offer в стиме с выбранными товарамии продайте их на торговой площадке Steam.  
    
Остались вопросы? Напишите @Noimf")

@dp.message(F.text.lower() == "поддержка")
async def send_support_info(message: Message) -> None:
    await message.answer(f"По вопросам пишите @Noimf")


@dp.callback_query(F.data == "TF2")
async def send_TF2_info(callback: CallbackQuery, state: FSMContext) -> None:
    proucts = ManageProducts().get_products()
    await state.set_state(Pay.product_name)
    kb_builder = InlineKeyboardBuilder()
    for product in proucts:
        if product.group == "TF2":
            market_TF2.append(product.name)
            kb_builder.add(InlineKeyboardButton(text=product.name, callback_data=product.name))
    kb = kb_builder.as_markup(resize_keyboard=True)
    await bot.send_message(callback.from_user.id, f"Выберите товар", reply_markup=kb)

@dp.callback_query(F.data == "CS2")
async def send_CS2_info(callback: CallbackQuery, state: FSMContext) -> None:
    products = ManageProducts().get_products()
    await state.set_state(Pay.product_name)
    kb_builder = InlineKeyboardBuilder()
    for product in products:
        if product.group == "CS2":
            market_CS2.append(product.name)
            kb_builder.add(InlineKeyboardButton(text=product.name, callback_data=product.name))
    kb = kb_builder.as_markup(resize_keyboard=True)
    await bot.send_message(callback.from_user.id, f"Выберите товар", reply_markup=kb)


@dp.callback_query(F.data.in_(market_TF2))
async def send_pay_info(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"product_name": callback.data})
    product = ManageProducts().get_product_by_name(callback.data)
    await bot.send_message(callback.from_user.id, f"Название товара: {product.name}\nЦена: {product.price} руб.\nКоличество: {product.quantity}\nСсылка на товар в стиме: {product.link}")
    await bot.send_message(callback.from_user.id, f"Выберите количество товара")
    await state.set_state(Pay.product_quantity)

@dp.callback_query(F.data.in_(market_CS2))
async def send_pay_info(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data({"product_name": callback.data})
    product = ManageProducts().get_product_by_name(callback.data)
    await bot.send_message(callback.from_user.id, f"Название товара: {product.name}\nЦена: {product.price} руб.\nКоличество: {product.quantity}\nСсылка на товар в стиме: {product.link}")
    await bot.send_message(callback.from_user.id, f"Выберите количество товара")
    await state.set_state(Pay.product_quantity)

@dp.message(Pay.product_quantity)
async def send_pay_info(message: Message, state: FSMContext) -> None:
    await state.update_data({"product_quantity": message.text})
    product_data = await state.get_data()
    product =ManageProducts().get_product_by_name(product_data.get("product_name"))
    if int(product_data.get("product_quantity")) > 0 and int(product_data.get("product_quantity")) <= int(product.quantity):
        await message.answer(f"Вы выбрали {product_data.get('product_quantity')} единиц товара {product.name}")
        await message.answer(f"Подтвердите покупку на {int(product_data.get('product_quantity')) * int(product.price)}", reply_markup=buy_kb)
    else:
        await message.answer(f"Вы ввели некорректное количество. Введите корректное количество единиц")


@dp.callback_query(F.data == "yes")
async def send_pay_info(callback: CallbackQuery, state: FSMContext) -> None:
    product_data = await state.get_data()
    product = ManageProducts().get_product_by_name(product_data.get("product_name"))
    admin = ManageAdmins().get_admins()
    user_data = ManageUsers().get_user_by_id(callback.from_user.id)
    if int(user_data.balance) >= int(product_data.get("product_quantity")) * int(product.price):
        ManageUsers().change_balance(user_data.user_id, -(int(product_data.get("product_quantity")) * int(product.price)))
        ManageUsers().change_deals(user_data.user_id, 1)
        ManageUsers().change_bonus(user_data.user_id, int(product_data.get("product_quantity")))
        ManageProducts().sell_product(product_data.get("product_name"), int(product_data.get("product_quantity")))
        await bot.send_message(callback.from_user.id, f"Оплата прошла успешно, скоро администратор отправвит вам trade offer.\nЗадержка может занять до 15 минут")
        product = ManageProducts().get_product_by_name(product_data.get("product_name"))
        for admin in admin:
            await bot.send_message(admin.user_id, f"Пользователь @{user_data.username} оплатил покупку\nТовар: {product.name}\nКоличество: {product_data.get('product_quantity')}\nЦена: {product.price}\nСумма: {int(product_data.get('product_quantity')) * int(product.price)}\nБаланс: {user_data.balance}\nTrade link: <a href = '{user_data.steam_link}'>{user_data.steam_name}</a>\nОстаток товара: {product.quantity}", reply_markup=start_kb, link_preview_options=options_1)
            await state.clear()
    else:
        await bot.send_message(callback.from_user.id, f"У вас недостаточно средств. Введите корректное количество единиц\nВаш баланс: {user_data.balance}")


        
    