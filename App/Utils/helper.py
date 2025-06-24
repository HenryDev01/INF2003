import string
import random
import bcrypt
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

from App.Utils import database
from flask_paginate import Pagination
from datetime import datetime


def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


def paginate_list(data_list, page, page_size, search):
    offset = (page - 1) * page_size
    paginated_data = data_list[offset:offset + page_size]
    pagination = Pagination(
        page=page,
        total=len(data_list),
        per_page=page_size,
        css_framework='bootstrap4',
        search=search,
        record_name=data_list
    )
    return paginated_data, pagination

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed_password.decode('utf-8')

def verify_password(password,hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))

def format_rating_count(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}k"
    else:
        return str(n)


def get_cart(customer_id):
    mongo_db = database.get_mongo_db()
    cart = mongo_db.cart.find_one({"customer_id": customer_id})
    if not cart:
        return {"customer_id": customer_id, "items": []}
    return cart

def save_cart(cart):
    mongo_db = database.get_mongo_db()
    cart["updated_at"] = datetime.now()
    mongo_db.cart.replace_one({"customer_id": cart["customer_id"]}, cart, upsert=True)


def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email