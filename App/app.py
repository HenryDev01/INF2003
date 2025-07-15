from collections import Counter
from flask import Flask, render_template, request, session
from flask_wtf import CSRFProtect
from datetime import datetime
from flask_mail import Mail, Message
from App.config import Config
from App.Models.ContactForm import  ContactForm
from App.Models import Inventory
from App.Models.Question import Question
from Utils.helper import paginate_list, format_rating_count, get_cart
from Utils import database
from Seller.routes import seller_bp
from Auth.routes import auth_bp
from Customer.routes import customer_bp
from flask_mail import Mail



app = Flask(__name__,template_folder='template')
app.config.from_object(Config)
app.register_blueprint(seller_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(auth_bp)

# csrf = CSRFProtect(app)
# csrf.init_app(app)
mail = Mail(app)


#SQL EXAMPLE:
# db  =database.get_sql_db()  # configure your sql db credential in get_sql_db() under Utils/database.py. Use mariaDB credential
# cursor = db.cursor()
# cursor.execute("SELECT * FROM STUDENT")
# data = cursor.fetchone()
# user = Users.User(data[3],data[3],data[3],data[3],data[3],data[3],data[3])
# print(user.get_nric())
# db.close()

#NOSQL
#db =database.get_mongo_db()  # configure your mongodb in get_mongo_db().

# information available to all routes
@app.context_processor
def inject_cart_info():
    cart_items = []
    cart_information = {}

    if session.get("customer_id"):
        sql_db = database.get_sql_db()
        cursor = sql_db.cursor()
        customer_cart = get_cart(session.get("customer_id"))
        cart_items = customer_cart.get("items", [])

        if cart_items:
            product_ids = [r.get("product_id") for r in cart_items]
            placeholders = ','.join(['%s'] * len(product_ids))
            sql = f"""
                   SELECT product_id, product_model, product_name, price, product_photo 
                   FROM product 
                   WHERE product_id IN ({placeholders})
               """
            cursor.execute(sql, product_ids)
            product_information = cursor.fetchall()

            cart_information = {
                row[0]: {
                    "product_id": row[0],
                    "product_model": row[1],
                    "product_name": row[2],
                    "product_price": row[3],
                    "product_photo": row[4]

                }
                for row in product_information
            }

    return dict(cart=cart_items, cart_information=cart_information)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/Product-details/<string:product_id>")
def single_product_details(product_id):
    # Retrieve product
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()
    cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    record = cursor.fetchone()
    product = Inventory.Product(*record)

    #retrieve review
    cursor.execute("SELECT order_id FROM order_items WHERE product_id = %s", (product_id,))
    existing_order_ids = [row[0] for row in cursor.fetchall()]
    mongo_db = database.get_mongo_db()
    review_collection = mongo_db["reviews"]
    query = {"order_id": {"$in":existing_order_ids}}
    reviews = list(review_collection.find(query).limit(5))
    if len(reviews) == 0:
        return render_template("customer/single-product-details.html", product = product, reviews = None, orderid_username = None )

    # review needs to get customer username
    order_ids = [doc["order_id"] for doc in reviews]
    placeholders = ','.join(['%s'] * len(order_ids))
    sql = f"SELECT orders.order_id, customer.username, customer.photo, customer.customer_id FROM orders,customer WHERE orders.customer_id = customer.customer_id AND orders.order_id IN ({placeholders})"
    cursor.execute(sql, order_ids)
    results = cursor.fetchall()
    orderid_username = {row[0]:{"username":row[1], "profile_image":row[2], "customer_id":row[3]} for row in results}

    #review statistics
    all_reviews = list(review_collection.find(query))
    review_scores = [r["review_score"] for r in all_reviews if
                     "review_score" in r and isinstance(r["review_score"], (int, float))]

    counts = Counter(review_scores)
    print(review_scores)
    if review_scores:
        average_rating = round(sum(review_scores) / len(review_scores), 1)

    total_review = len(all_reviews)
    total_ratings = format_rating_count(sum(review_scores))

    review_statistic = {}
    review_statistic["total_review"] = total_review
    review_statistic["average"] = average_rating
    review_statistic["total_ratings"] = total_ratings
    review_statistic["five_star_percentage"] = (counts.get(5, 0) / total_review) * 100 if total_review else 0
    review_statistic["four_star_percentage"] = (counts.get(4, 0) / total_review) * 100 if total_review else 0
    review_statistic["three_star_percentage"] = (counts.get(3, 0) / total_review) * 100 if total_review else 0
    review_statistic["two_star_percentage"] = (counts.get(2, 0) / total_review) * 100 if total_review else 0
    review_statistic["one_star_percentage"] = (counts.get(1, 0) / total_review) * 100 if total_review else 0

    sql_db.close()
    return render_template("customer/single-product-details.html", product = product, reviews = reviews, orderid_username = orderid_username, review_statistic=review_statistic )

@app.route('/')
def index():

    return render_template('Customer/index.html' )


@app.route('/Product/<string:category>')
def Product(category):
    sort_requirement = request.args.get('sort_by')
    max_price = request.args.get('max_price')
    min_price = request.args.get('min_price')
    action = request.args.get("action")

    db = database.get_sql_db()
    cursor = db.cursor()
    mongo_db = database.get_mongo_db()
    review_collection = mongo_db["reviews"]

    #get category
    cursor.execute("SELECT product_category_translation FROM category_translation ORDER BY product_category_translation")
    categories = cursor.fetchall()
    print(categories)

    #build mongodb query
    rating_pipeline = [
        {
            "$group": {
                "_id": "$product_id",
                "avg_rating": {"$avg": "$review_score"},
                "total_review": {"$sum": 1},
                "total_rating": {"$sum": "$review_score"}
            }
        }
    ]
    rating_data = review_collection.aggregate(rating_pipeline)
    rating_map = {r["_id"]: r for r in rating_data}

    # build sql statements
    sql = "SELECT * FROM product"
    param = []
    if action == "apply":
        if max_price and min_price :
            sql += " WHERE price >= %s AND price <= %s"
            param.extend([min_price,max_price])

        if sort_requirement == "descending":
            sql += " ORDER BY price desc"
        elif sort_requirement == "ascending":
            sql += " ORDER BY price"

    cursor.execute(sql,param)
    records = cursor.fetchall()
    db.close()

    products = []
    for product in records:
        p = Inventory.Product(*product)
        rating = rating_map.get(p.get_product_id(),{}).get("avg_rating",0)
        p.set_rating(rating)
        products.append(p)

    if sort_requirement == "highest_rated":
        products.sort(key=lambda p:p.get_rating(), reverse=True)



    # page configuration
    page_size = 9
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = int(request.args.get('page', 1))

    # display products can be shown per page
    product_paged ,pagination = paginate_list(products,page,page_size,search)

    return render_template('Customer/shop.html' , active = 'Product', pagination=pagination, categories=categories,category=category, count=len(products), productsList=product_paged, review_statistic = rating_map)






#
@app.route('/support', methods=['POST', 'GET'])
def support():

    form = ContactForm()
    if request.method == "POST":
        send_message({"message":form.message.data})
    q1 = Question("How long does shipping usually take?","test","test","test")
    q1.set_display("Yes")
    q1.set_answer("Shipping typically takes 3-7 business days for standard delivery. Expedited options are available at checkout for faster delivery.")

    q2 = Question("How long does it takes to deliver to the Customer?","test","test","test")
    q2.set_display("Yes")
    q2.set_answer("This depends on whether the product is in stock. In the situation where product is out of stock we may contact you to change or refund.")

    questionList = []
    questionList.append(q1)
    questionList.append(q2)

    return render_template('Customer/support.html', active ='Contact',form=form,questionList=questionList )

def send_message(message):
    print(message.get('name'))

    msg = Message(message.get('subject'), sender=message.get('email'),
                  recipients=['pietoncharm@gmail.com'],
                  body=message.get('message')
                  )
    mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True)

