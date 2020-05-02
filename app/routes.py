from app import application, engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin

CORS(application,support_credentials=True)
Base = automap_base()
Base.prepare(engine, reflect=True)
Accounts = Base.classes.account
Books = Base.classes.books
session = Session(engine)
metadata = MetaData(engine)


@application.route('/index')
@application.route('/')
def index():
    return 'Welcome to this page'


@application.route('/register', methods=["GET","POST"])
def register():
    username = request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    password_hash = generate_password_hash(password)
    account = Table('account', metadata, autoload=True)
    engine.execute(account.insert(), username=username,
                   email=email, password=password_hash)
    return jsonify({'user_added': True})


@application.route('/sign_in', methods=["GET","POST"])
def sign_in():
    username_entered = request.args.get('username')
    password_entered = request.args.get('password')
    user = session.query(Accounts).filter(or_(Accounts.username == username_entered, Accounts.email == username_entered)
                                          ).first()
    if user is not None and check_password_hash(user.password, password_entered):
        return jsonify({'signed_in': True})
    return jsonify({'signed_in': False})


@application.route('/add_book', methods=["GET","POST"])
def add_book():
    isbn = request.args.get('isbn')
    book_title = request.args.get('book_title')
    book_author = request.args.get('book_author')
    publication_year = request.args.get('publication_year')
    image_url = request.args.get('image_url')
    books = Table('books', metadata, autoload=True)
    engine.execute(books.insert(), isbn=isbn,
                   book_title=book_title, book_author=book_author, publication_year=publication_year,
                   image_url=image_url)
    return jsonify({'book_added': True})


@application.route('/fetch_books', methods=["GET","POST"])
def fetch_books():
    books = session.query(Books).all()
    books_list = []
    for book in books:
        books_list.append({
            'isbn': book.isbn,
            'book_title': book.book_title,
            'book_author': book.book_author,
            'publication_year': book.publication_year,
            'image_url': book.image_url
        })
    return jsonify(books_list)