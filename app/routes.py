from app import application, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin


Base = automap_base()
Base.prepare(engine, reflect=True)
Accounts = Base.classes.account
session = Session(engine)


@application.route('/index')
@application.route('/')
def index():
    return 'Welcome to this page'


@application.route('/register', methods=['GET', 'POST','OPTIONS'])
@cross_origin()
def register():
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    password_hash = generate_password_hash(password)
    metadata = MetaData(engine)
    account = Table('account', metadata, autoload=True)
    engine.execute(account.insert(), username=username,
                   email=email, password=password_hash)
    return jsonify({'user_added': True})


@application.route('/sign_in', methods=['GET', 'POST','OPTIONS'])
@cross_origin()
def sign_in():
    username_entered = request.args.get('username')
    password_entered = request.args.get('password')
    user = session.query(Accounts).filter(or_(Accounts.username == username_entered, Accounts.email == username_entered)
                                          ).first()
    if user is not None and check_password_hash(user.password, password_entered):
        return jsonify({'signed_in': True})
    return jsonify({'signed_in': False})
