from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS, cross_origin


# Initialization
application = Flask(__name__)
application.config.from_object(Config)
CORS(application, resources={r"/*": {"origins": "*"}}, support_credentials=True)


DB_URI = application.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DB_URI)

from app import routes