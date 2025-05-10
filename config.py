class Config:
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/otopark_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
