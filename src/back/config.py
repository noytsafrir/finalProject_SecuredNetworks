class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/store'   # TODO change to your root password 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PASSWORD_LENGTH = 10
    LAST_PASSWORDS_COUNT = 3
    LOGIN_ATTEMPTS_LIMIT = 3
    DICTIONARY_WORDS = ['password1!', 'Aa1234567!', 'abcd12345!']
    CONTAIN_UPPERCASE = True
    CONTAIN_LOWERCASE = True
    CONTAIN_NUMERIC = True
    CONTAIN_SPECIAL = True
