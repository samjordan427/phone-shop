from datetime import datetime
from shop import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    phones = db.relationship('Phone', backref='manufacturer', lazy=True)

    def __repr__(self):
        return f"Manufacturer('{self.name}')"

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(120), nullable=False)
    mass = db.Column(db.Numeric(10,2), nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Numeric(10,2), nullable=False)
    image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
    stock_level = db.Column(db.Integer, nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)

    def __repr__(self):
        return f"Phone('{self.model}', '{self.description}', '{self.mass}', '{self.ram}', '{self.publication_date}', '{self.price}', '{self.stock_level}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    phone_id = db.Column(db.Integer, db.ForeignKey('phone.id'), nullable=False)

    def __repr__(self):
        return f"Cart('{self.quantity}')"
