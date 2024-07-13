import os, mysql.connector
from dotenv import load_dotenv
from models import User
from config import Config
from validator import *


load_dotenv()
safe_mode = os.getenv('SAFE_MODE') == 'true'

def check_user(email):
    user = User.query.filter_by(email=email).first()
    return user is not None

def check_password(user, password):
    return user.check_password(password)

def password_configuration(email,password):
    if(is_password_complex(password) == False or
        is_dictionary_word(password) == True or
        is_password_new(email, password) == False):
        return False
    return True

def set_unsecured_connection():
    # Database connection setup
    unsecuredConnection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=Config.DB_PASSWORD,
        database='store'
    )
    unsecuredCursor = unsecuredConnection.cursor()
    return unsecuredConnection, unsecuredCursor

def close_unsecured_connection(cursor, connection):
    connection.commit()
    cursor.close()
    connection.close()