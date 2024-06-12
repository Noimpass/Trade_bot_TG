from db.models import *
from db.dataspace import *
from db.db import *
from request.request import *

product = Product(
    name="Кейс «Киловатт»",
    group="CS2",
    price=100,
    quantity=100
)

User = Users(
    username="test",
    user_id=1,
    balance=1,
    deals=1,
    bonus=1,
    trade_link="test"
)

Admin = Admins(
    username="test",
    user_id=1
)

#ManageProducts().add_product(product)
#ManageUsers().add_user(User)
#ManageAdmins().add_admin(Admin)

ManageAdmins().get_admins()
products = ManageProducts().get_products()
ManageUsers().get_users()

for product in products:
    print(product.name)