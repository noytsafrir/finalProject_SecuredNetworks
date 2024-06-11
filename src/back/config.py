class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/store'   # TODO change to your root password 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO - update to cloud based db