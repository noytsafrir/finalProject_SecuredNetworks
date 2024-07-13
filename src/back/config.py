class Config:
    DB_PASSWORD = "A123456" # TODO change to your root password 
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{DB_PASSWORD}@localhost/store'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PASSWORD_LENGTH = 10
    LAST_PASSWORDS_COUNT = 3
    LOGIN_ATTEMPTS_LIMIT = 3
    DICTIONARY_WORDS = ['password1!', 'Aa1234567!', 'abcd12345!']
    CONTAIN_UPPERCASE = True
    CONTAIN_LOWERCASE = True
    CONTAIN_NUMERIC = True
    CONTAIN_SPECIAL = True
