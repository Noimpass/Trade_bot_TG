from db.models import *
from db.dataspace import *
from db.db import *
from request.request import *

product = Product(
    name="Mann Co. Supply Crate Key",
    group="TF2",
    price=100,
    quantity=100,
    link="await"
)

service = Service(
    name="test",
    price=100,
)

User = Users(
    username="test",
    user_id=1,
    balance=1,
    deals=1,
    bonus=1,
    trade_link=None,
    steam_link=None,
    steam_name=None
)

Admin = Admins(
    username="test",
    user_id=1
)

#ManageProducts().add_product(product)
#ManageUsers().add_user(User)
#ManageAdmins().add_admin(Admin)
ManageServices().add_service(service)

admins =ManageAdmins().get_admins()
products = ManageProducts().get_products()
users = ManageUsers().get_users()
services = ManageServices().get_services()

for admin in admins:
    print(admin.username)

for user in users:
    print(user.username)

for service in services:
    print(service.name)
    
for product in products:
    print(product.name)