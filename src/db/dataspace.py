from db import db
from db.models import *
from sqlalchemy.exc import NoResultFound
from config import settings
import logging

session = db.create_database()


class ManageAdmins:
    def get_admins(self):
        try:
            admins = session.query(Admins).all()
            return admins
        except NoResultFound:
            return None
    
    def get_admin_by_id(self, user_id: int):
        try:
            admin = session.query(Admins).filter(Admins.user_id == user_id).one()
            return admin
        except NoResultFound:
            return None
        
    def add_admin(self, admin:Admins):
        try:
            session.add(admin)
            session.commit()
        except Exception:
            logging.error("Can't add admin", Exception)
            

class ManageUsers:
    def get_users(self):
        try:
            users = session.query(Users).all()
            return users
        except NoResultFound:
            return None
    
    def get_user_by_id(self, user_id: int):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            return user
        except NoResultFound:
            return None
        
    def add_user(self, user:Users):
        try:
            session.add(user)
            session.commit()
        except Exception:
            logging.error("Can't add user", Exception)

    def change_trade_link(self, user_id: int, trade_link: str):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            user.trade_link = trade_link
            session.commit()
        except Exception:
            logging.error("Can't change trade link", Exception)

    def change_steam_link(self, user_id: int, steam_link: str):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            user.steam_link = steam_link
            session.commit()
        except Exception:
            logging.error("Can't change steam link", Exception)

    def change_steam_name(self, user_id: int, steam_name: str):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            user.steam_name = steam_name
            session.commit()
        except Exception:
            logging.error("Can't change steam name", Exception)

    def change_balance(self, user_id: int, balance: int):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            user.balance = user.balance + balance
            session.commit()
        except Exception:
            logging.error("Can't change balance", Exception)

    def change_deals(self, user_id: int, deals: int):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            user.deals = user.deals + deals
            session.commit()
        except Exception:
            logging.error("Can't change deals", Exception)
    
    def change_bonus(self, user_id: int, bonus: int):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            user.bonus = user.bonus + bonus
            session.commit()
        except Exception:
            logging.error("Can't change bonus", Exception)
    
class ManageProducts:
    def get_products(self):
        try:
            products = session.query(Product).all()
            return products
        except NoResultFound:
            return None
        
    def get_product_by_id(self, product_id: int):
        try:
            product = session.query(Product).filter(Product.id == product_id).one()
            return product
        except NoResultFound:
            return None
        
    def get_product_by_name(self, product_name: str):
        try:
            product = session.query(Product).filter(Product.name == product_name).one()
            return product
        except NoResultFound:
            return None
        
    def add_product(self, product:Product):
        try:
            session.add(product)
            session.commit()
        except Exception as e:
            logging.error("Can't add product", e)

    def delete_product(self, product_name: str):
        try:
            product = session.query(Product).filter(Product.name == product_name).one()
            session.delete(product)
            session.commit()
        except Exception as e:
            logging.error("Can't delete product", e)

    def change_price(self, product_name: str, price: int):
        try:
            product = session.query(Product).filter(Product.name == product_name).one()
            product.price = price
            session.commit()
        except Exception as e:
            logging.error("Can't change price", e)

    def change_quantity(self, product_name: str, quantity: int):
        try:
            product = session.query(Product).filter(Product.id == product_name).one()
            product.quantity = quantity
            session.commit()
        except Exception as e:
            logging.error("Can't change quantity", e)

    def sell_product(self, product_name: str, quantity: int):
        try:
            product = session.query(Product).filter(Product.name == product_name).one()
            product.quantity = product.quantity - quantity
            session.commit()
        except Exception as e:
            logging.error("Can't sell product", e)
        

class ManageServices:
    def get_services(self):
        try:
            services = session.query(Service).all()
            return services
        except NoResultFound:
            return None
        
    def get_service_by_id(self, service_id: int):
        try:
            service = session.query(Service).filter(Service.id == service_id).one()
            return service
        except NoResultFound:
            return None
        
    def get_service_by_name(self, service_name: str):
        try:
            service = session.query(Service).filter(Service.name == service_name).one()
            return service
        except NoResultFound:
            return None
        
    def add_service(self, service:Service):
        try:
            session.add(service)
            session.commit()
        except Exception as e:
            logging.error("Can't add service", e)

    def delete_service(self, service_name: str):
        try:
            service = session.query(Service).filter(Service.name == service_name).one()
            session.delete(service)
            session.commit()
        except Exception as e:
            logging.error("Can't delete service", e)

    def change_price(self, service_name: str, price: int):
        try:
            service = session.query(Service).filter(Service.name == service_name).one()
            service.price = price
            session.commit()
        except Exception as e:
            logging.error("Can't change price", e)

