from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    change_link = State()

class AddProduct(StatesGroup):
    add_product_name = State()
    add_product_group = State()
    add_product_price = State()
    add_product_quantity = State() 