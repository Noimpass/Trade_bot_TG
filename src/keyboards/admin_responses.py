import logging

from dispatcher import dp, bot
from aiogram import types, html, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, LinkPreviewOptions
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards.menu import *
from keyboards.state import *
from keyboards.admin_menu import *
from db.dataspace import ManageUsers, ManageAdmins, ManageProducts
from db.models import Users


options_1 = LinkPreviewOptions(is_disabled=True)

admins = ManageAdmins().get_admins()

@dp.message(F.command("admin") and F.user_id in admins)
async def send_admin_menu(message: Message) -> None:
    await message.answer(f"Меню администратора", reply_markup=admin_kb)

@dp.message(F.text.lower() == "редактировать товары" and F.user_id in admins)
async def send_admin_menu(message: Message) -> None:
    products = ManageProducts().get_all_products()
    for product in products:
        await bot.send_message(message.from_user.id, f"Название: {product.name}\nГруппа: {product.group}\nЦена: {product.price}\nКоличество: {product.quantity}\n",reply_markup=admin_menu_kb)

@dp.message(F.text.lower() == "Добавить товар" and F.user_id in admins)
async def send_admin_menu(message: Message, state: FSMContext) -> None:
    state.set_state(AddProduct.add_product_name)
    await message.answer(f"Вввведите название")

@dp.message(AddProduct.add_product_name and F.user_id in admins)
async def add_product_name(message: Message, state: FSMContext) -> None:
    state.set_data({"product_name": message.text})
    await message.answer(f"Вввведите группу")
    state.set_state(AddProduct.add_product_group)

@dp.message(AddProduct.add_product_group and F.user_id in admins)
async def add_product_group(message: Message, state: FSMContext) -> None:
    state.set_data({"product_group": message.text})
    await message.answer(f"Вввведите цену")
    state.set_state(AddProduct.add_product_price)

@dp.message(AddProduct.add_product_price and F.user_id in admins)
async def add_product_price(message: Message, state: FSMContext) -> None:
    state.set_data({"product_price": message.text})
    await message.answer(f"Введите количество")
    state.set_state(AddProduct.add_product_quantity)

@dp.message(AddProduct.add_product_quantity and F.user_id in admins)
async def add_product_quantity(message: Message, state: FSMContext) -> None:
    state.set_data({"product_quantity": message.text})
    product = state.get_data()
    ManageProducts().add_product(product["product_name"], product["product_group"], product["product_price"], product["product_quantity"])
    await message.answer(f"Товар добавлен")

@dp.message(F.text.lower() == "меню пользователя" and F.user_id in admins) 
async def send_user_menu(message: Message) -> None:
    await message.answer(f"Меню пользователя", reply_markup=start_admin_kb)