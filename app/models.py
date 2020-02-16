from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
# import jwt
from app import app, db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(250))
    orders = db.relationship("Order", back_populates="user")

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    meals = db.relationship("Meal", back_populates="category")

    def __repr__(self):
        return f'<Category {self.id}: {self.title}>'


meals_orders_table = db.Table('meals_orders',
                              db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
                              db.Column('order_id', db.Integer, db.ForeignKey('orders.id')))


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    picture = db.Column(db.String(64), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="meals")
    orders = db.relationship("Order", secondary=meals_orders_table, back_populates="meals")

    def __repr__(self):
        return f'<Meal {self.id}: {self.title} {self.picture}>'


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("order_states.id"))
    state = db.relationship("OrderState", back_populates="orders")
    meals = db.relationship("Meal", secondary=meals_orders_table, back_populates="orders")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="orders")

    def __repr__(self):
        return f'<Order {self.id}: {self.user.username} - {self.amount} [{", ".join([m.title for m in self.meals])}]>'


class OrderState(db.Model):
    __tablename__ = "order_states"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    orders = db.relationship("Order", back_populates="state")

    def __repr__(self):
        return f'<Category {self.id}: {self.title}>'


db.create_all()
