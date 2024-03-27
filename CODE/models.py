from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


###############<--!DB MODELS!-->################

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String, unique=True, nullable=False)
    name= db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    phone= db.Column(db.Integer, unique=True, nullable=False)
    address= db.Column(db.String, nullable=True)
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')


    def cart_items_total_price(self):
        cart_items = self.cart_items
        total_price = sum(item.item.price * item.quantity for item in cart_items)
        return total_price

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', name='{self.name}', is_admin={self.is_admin}, phone={self.phone}, address='{self.address}')"

# All items that are added or delted by the Admin only
class GroceryItem(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    price= db.Column(db.Float, nullable=False)
    category= db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

# User's whole Order with all the items and stuff
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True ,cascade='all, delete-orphan')
    purchase_date = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return f"(id={self.id}, user_id={self.user_id}, total_price={self.total_price}, items={self.items}, purchase_date={self.purchase_date})"

# Order individual item model to store individual items in an order
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    grocery_item_id = db.Column(db.Integer, db.ForeignKey('grocery_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"(id={self.id}, order_id={self.order_id}, grocery_item_id={self.grocery_item_id}, quantity={self.quantity}, price={self.price}, total_price={self.total_price})"
    

# User's cart storing model that stores all carts, Even if one item is in cart for any user, you wont be able to delete that item from the  Grocery Item table 
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery_item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    item = db.relationship('GroceryItem', backref=db.backref('cart_items', lazy=True))

