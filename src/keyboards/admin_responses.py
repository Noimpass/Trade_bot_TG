import logging

from functools import wraps
from dispatcher import dp, bot
from aiogram import types, html, F
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards.menu import *
from keyboards.state import *
from keyboards.admin_menu import *
from db.dataspace import ManageUsers, ManageAdmins, ManageProducts
from db.models import Users, Product


options_1 = LinkPreviewOptions(is_disabled=True)

admins = ManageAdmins().get_admins()
def admins_only(handler):
    @wraps(handler)
    async def handler_wrapper(message: Message, *args, **kwargs):
        if message.from_user.id in [admin.user_id for admin in admins]:
            return await handler(message, *args, **kwargs)
        else:
            return await message.answer("Ты не админ")
    return handler_wrapper


@dp.message((Command("admin")))
@admins_only
async def send_admin_menu(message: Message) -> None:
    await message.answer(f"Меню администратора", reply_markup=admin_kb)

@dp.message((F.text.lower() == "редактировать товары"))
@admins_only
async def send_products(message: Message) -> None:
    products = ManageProducts().get_products()
    for product in products:
        await message.answer(f"Название: {product.name}\nГруппа: {product.group}\nЦена: {product.price}\nКоличество: {product.quantity}\n",reply_markup=product_menu_kb)

@dp.message((F.text.lower() == "добавить товар"))
@admins_only
async def add_product(message: Message, state: FSMContext) -> None:
    await state.set_state(AddProduct.add_product_name)
    await message.answer(f"Вввведите название")

@dp.message(AddProduct.add_product_name)
async def add_product_name(message: Message, state: FSMContext) -> None:
    await state.update_data({"add_product_name": message.text})
    await message.answer(f"Вввведите группу")
    await state.set_state(AddProduct.add_product_group)

@dp.message(AddProduct.add_product_group)
async def add_product_group(message: Message, state: FSMContext) -> None:
    await state.update_data({"add_product_group": message.text})
    await message.answer(f"Вввведите цену")
    await state.set_state(AddProduct.add_product_price)

@dp.message(AddProduct.add_product_price)
async def add_product_price(message: Message, state: FSMContext) -> None:
    await state.update_data({"add_product_price": message.text})
    await message.answer(f"Введите количество")
    await state.set_state(AddProduct.add_product_quantity)

@dp.message(AddProduct.add_product_quantity)
async def add_product_quantity(message: Message, state: FSMContext) -> None:
    await state.update_data({"add_product_quantity": message.text})
    await message.answer(f"Вввведите ссылку на товар")
    await state.set_state(AddProduct.add_product_link)

@dp.message(AddProduct.add_product_link)
async def add_product_link(message: Message, state: FSMContext) -> None:
    await state.update_data({"add_product_link": message.text})
    product_data = await state.get_data()
    product = Product(
        name=product_data.get("add_product_name"),
        group=product_data.get("add_product_group"),
        price=product_data.get("add_product_price"),
        quantity=product_data.get("add_product_quantity"),
        link=product_data.get("add_product_link"),
    )
    ManageProducts().add_product(product)
    await message.answer(f"Товар добавлен")
    await state.clear()

@dp.message(F.text.lower() == "удалить товар")
@admins_only
async def delete_product(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteProduct.delete_product_name)
    await message.answer(f"Вввведите название товара")

@dp.message(DeleteProduct.delete_product_name)
async def delete_product_name(message: Message, state: FSMContext) -> None:
    await state.update_data({"product_name": message.text})
    product = await state.get_data()
    ManageProducts().delete_product(product.get("product_name"))
    await message.answer(f"Товар удален")
    await state.clear()

@dp.message(F.text.lower()=="изменить цену")
@admins_only
async def change_price(message: Message, state: FSMContext) -> None:
    await state.set_state(ChangePrice.change_price_name)
    await message.answer(f"Вввведите название товара")

@dp.message(ChangePrice.change_price_name)
async def change_price_name(message: Message, state: FSMContext) -> None:
    await state.update_data({"product_name": message.text})
    await message.answer(f"Вввведите цену")
    await state.set_state(ChangePrice.change_price)

@dp.message(ChangePrice.change_price)
async def change_price(message: Message, state: FSMContext) -> None:
    await state.update_data({"product_price": message.text})
    product = await state.get_data()
    ManageProducts().change_price(product.get("product_name"), product.get("product_price"))
    await message.answer(f"Цена изменена")
    await state.clear()

@dp.message(F.text.lower() == "изменить количество")
@admins_only
async def change_quantity(message: Message, state: FSMContext) -> None:
    await state.set_state(ChangeQuantity.change_quantity_name)
    await message.answer(f"Вввведите название товара")

@dp.message(ChangeQuantity.change_quantity_name)
async def change_quantity_name(message: Message, state: FSMContext) -> None:
    await state.update_data({"product_name": message.text})
    await message.answer(f"Введите количество")
    await state.set_state(ChangeQuantity.change_quantity)

@dp.message(ChangeQuantity.change_quantity)
async def change_quantity(message: Message, state: FSMContext) -> None:
    await state.update_data({"product_quantity": message.text})
    product = await state.get_data()
    ManageProducts().change_quantity(product.get("product_name"), product.get("product_quantity"))
    await message.answer(f"Количество изменено")
    await state.clear()
    
      
@dp.message(F.text.lower() == "назад")
@admins_only
async def send_admin_menu(message: Message) -> None:
    await message.answer(f"Меню администратора", reply_markup=admin_kb)

@dp.message(F.text.lower() == "меню пользователя")
@admins_only 
async def send_user_menu(message: Message) -> None:
    await message.answer(f"Меню пользователя", reply_markup=start_kb)

