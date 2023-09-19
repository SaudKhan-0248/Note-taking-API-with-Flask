from dotenv import load_dotenv
import os

load_dotenv()


class Setting():
    secret_key = os.getenv('SECRET_KEY')
    sqlalchemy_database_url = os.getenv('SQLALCHEMY_DATABASE_URL')
    jwt_secret_key = os.getenv('JWT_SECRET_KEY')
    redis_host = os.getenv('REDIS_HOST')


settings = Setting()
