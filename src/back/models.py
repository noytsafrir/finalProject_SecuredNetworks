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

    def set_password(self, password): #לבדוק האם זה תואם לחלק שלהם 
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
