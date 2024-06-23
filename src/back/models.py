# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
import os

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)

class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    login_attempts = db.Column(db.Integer, default=0)
    password_history = db.relationship('PasswordHistory', backref='user', lazy=True)

    def set_password(self, password): #לבדוק האם זה תואם לחלק שלהם 
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
    
    def increment_login_attempts(self):
        self.login_attempts += 1
        db.session.commit()

    def reset_login_attempts(self):
        self.login_attempts = 0
        db.session.commit()

# class PasswordHistory(db.Model):
#     email = db.Column(db.String(255), primary_key=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     timestamp = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True)

#     def set_password(self, password):
#         self.password_hash = password

class PasswordHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), primary_key=False, nullable=False)

    def set_password(self, password):
        self.password_hash = password
