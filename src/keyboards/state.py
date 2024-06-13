from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    change_link = State()

class AddProduct(StatesGroup):
    add_product_name = State()
    add_product_group = State()
    add_product_price = State()
    add_product_quantity = State() 
    add_product_link = State()

class DeleteProduct(StatesGroup):
    delete_product_name = State()

class ChangePrice(StatesGroup):
    change_price_name = State()
    change_price = State()

class ChangeQuantity(StatesGroup):
    change_quantity_name = State()
    change_quantity = State()

class Pay(StatesGroup):
    product_name = State()
    product_quantity = State()

class Deposit(StatesGroup):
    deposit_amount = State()