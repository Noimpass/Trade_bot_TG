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
from db.dataspace import *
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
    await state.update_data(В)
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
    
#=========================================Услуги=========================================
@dp.message((F.text.lower() == "редактировать услуги"))
async def send_services(message: Message) -> None:
    services = ManageServices().get_services()
    for service in services:
        await message.answer(f"Название: {service.name}\nЦена: {service.price}\n",reply_markup=service_menu_kb)

@dp.message((F.text.lower() == "добавить услугу"))
@admins_only
async def add_service(message: Message, state: FSMContext) -> None:
    await state.set_state(AddService.add_service_name)
    await message.answer(f"Вввведите название")

@dp.message(AddService.add_service_name)
async def add_service_name(message: Message, state: FSMContext) -> None:
    await state.update_data({"add_service_name": message.text})
    await message.answer(f"Вввведите цену")
    await state.set_state(AddService.add_service_price)

@dp.message(AddService.add_service_price)
async def add_service_price(message: Message, state: FSMContext) -> None:
    await state.update_data({"add_service_price": message.text})
    service_data = await state.get_data()
    service = Service(
        name=service_data.get("add_service_name"),
        price=service_data.get("add_service_price"),
    )
    ManageServices().add_service(service)
    await message.answer(f"Услуга добавлена")
    await state.clear()

@dp.message(F.text.lower() == "удалить услугу")
@admins_only
async def delete_service(message: Message, state: FSMContext) -> None:
    await state.set_state(DeleteService.delete_service_name)
    await message.answer(f"Вввведите название услуги")

@dp.message(DeleteService.delete_service_name)
async def delete_service_name(message: Message, state: FSMContext) -> None:
    await state.update_data({"service_name": message.text})
    service = await state.get_data()
    ManageServices().delete_service(service.get("service_name"))
    await message.answer(f"Услуга удалена")
    await state.clear()

@dp.message(F.text.lower() == "изменить цену услуги")
@admins_only
async def change_price(message: Message, state: FSMContext) -> None:
    await state.set_state(ChangeServicePrice.change_service_name)
    await message.answer(f"Вввведите название услуги")

@dp.message(ChangeServicePrice.change_service_name)
async def change_price_name(message: Message, state: FSMContext) -> None:
    await state.update_data({"service_name": message.text})
    await message.answer(f"Вввведите цену")
    await state.set_state(ChangeServicePrice.change_service_price)

@dp.message(ChangeServicePrice.change_service_price)
async def change_price(message: Message, state: FSMContext) -> None:
    await state.update_data({"service_price": message.text})
    service = await state.get_data()
    ManageServices().change_price(service.get("service_name"), service.get("service_price"))
    await message.answer(f"Цена изменена")
    await state.clear()

@dp.message(F.text.lower() == "назад")
@admins_only
async def send_admin_menu(message: Message, state: FSMContext) -> None:
    await message.answer(f"Меню администратора", reply_markup=admin_kb)
    await state.clear()

@dp.message(F.text.lower() == "меню пользователя")
@admins_only 
async def send_user_menu(message: Message) -> None:
    await message.answer(f"Меню пользователя", reply_markup=start_kb)

