import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key_pizzeria'
    
    USER = 'root'
    PASSWORD = 'root' 
    HOST = 'localhost'
    DATABASE = 'pizzeria'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'   
    SQLALCHEMY_TRACK_MODIFICATIONS = False