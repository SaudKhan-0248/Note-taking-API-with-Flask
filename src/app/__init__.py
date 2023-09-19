from flask import Flask
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import redis
from .models import Base
from .settings import settings
from .routes import auth, notes, users

app = Flask(__name__)
jwt = JWTManager(app)
redis_client = redis.Redis(host=settings.redis_host, port=6379,
                           db=0, decode_responses=True)
cors = CORS(app)

# Configuration
app.config['SECRET_KEY'] = settings.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = settings.sqlalchemy_database_url
app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key
SWAGGER_URL = '/api/docs'
API_URL = '/static/openapi.yml'

# Connecting to Database
if not database_exists(settings.sqlalchemy_database_url):
    create_database(settings.sqlalchemy_database_url)

engine = create_engine(settings.sqlalchemy_database_url)
Base.metadata.create_all(bind=engine)
session = Session(engine)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Notes API"
    }
)

# Registering Blueprints
app.register_blueprint(auth.auth)
app.register_blueprint(notes.notes)
app.register_blueprint(users.users)
app.register_blueprint(swaggerui_blueprint)
