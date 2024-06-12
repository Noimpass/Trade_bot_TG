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
    
    def change_balance(self, user_id: int, balance: int):
        try:
            user = session.query(Users).filter(Users.user_id == user_id).one()
            user.balance = balance
            session.commit()
        except Exception:
            logging.error("Can't change balance", Exception)

    

class ManageProducts:
    def get_products(self):
        try:
            products = session.query(Product).all()
            return products
        except NoResultFound:
            return None
        
    def add_product(self, product:Product):
        try:
            session.add(product)
            session.commit()
        except:
            logging.error("Can't add product", product)

    def delete_product(self, product_id: int):
        try:
            product = session.query(Product).filter(Product.id == product_id).one()
            session.delete(product)
            session.commit()
        except:
            logging.error("Can't delete product", product)

    def change_quantity(self, product_id: int, quantity: int):
        try:
            product = session.query(Product).filter(Product.id == product_id).one()
            product.quantity = quantity
            session.commit()
        except:
            logging.error("Can't change quantity", product)
        
