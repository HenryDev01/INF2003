import os
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, jsonify, session, request, flash
from werkzeug.utils import secure_filename

from App.Models.Inventory import Product
from App.Models.Order import Order
from App.Utils import database
from App.Utils.helper import get_cart, save_cart, paginate_list
from App.Models.Users import Customer

customer_bp = Blueprint("Customer",__name__)

@customer_bp.route('/customer_profile')
def customer_profile():
    customer_id = session.get("customer_id")
    if customer_id is None:
        return redirect(url_for("auth.login"))

    db = database.get_sql_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
    row = cursor.fetchone()
    customer = Customer(*row)

    return render_template('Customer/customer_profile.html', customer=customer)




@customer_bp.route('/checkout')
def checkout():
    selected_items = session.get("selected_items_for_checkout")
    if not session.get("customer_id") or not selected_items:
        return redirect(url_for("index"))

    #customer information
    print(selected_items)
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (session.get("customer_id"),))
    customer_data = cursor.fetchone()
    customer = Customer(*customer_data)

    #product information
    product_ids = [item['product_id'] for item in selected_items]  # ['P002']
    placeholders = ','.join(['%s'] * len(product_ids))  # "%s" if 1 item, "%s,%s" for 2, etc.
    sql = f"SELECT * FROM product WHERE product_id IN ({placeholders})"
    cursor.execute(sql, product_ids)
    product_info = cursor.fetchall()
    products = [Product(*row) for row in product_info]
    quantity_map = {item["product_id"]: item["quantity"] for item in selected_items}
    print(products)

    return render_template('Customer/checkout.html', customer = customer, products = products, quantity_map = quantity_map)



# <string:status> - all, pending, cancelled, delivered
# /customer_order/all to access webpage
@customer_bp.route('/customer_order/<string:status>',methods=['POST','GET'])
def customer_order(status):
    # TODO: Implement user who logged in to be able to view their own order only.
    print(status)
    if session.get("customer_id") is None:
        return redirect(url_for("auth.login"))


    customer_id = session.get("customer_id")
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    # Fetch orders for the logged-in customer by status
    if status == 'all':
        sql = """ SELECT o.order_id, o.customer_id, o.order_purchase_timestamp, oi.product_id,  COUNT(*) as quantity, p.product_name, p.price, p.product_description, o.shipping_address, o.shipping_postal_code, o.order_status, o.order_estimated_delivery_date, o.order_purchase_timestamp  FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN product p ON oi.product_id = p.product_id WHERE o.customer_id = %s GROUP BY p.product_id ORDER BY o.order_purchase_timestamp DESC"""
        cursor.execute(sql, (customer_id,))

    else:
        sql = """ SELECT o.order_id, o.customer_id, o.order_purchase_timestamp, oi.product_id,  COUNT(*) as quantity, p.product_name, p.price, p.product_description, o.shipping_address, o.shipping_postal_code, o.order_status, o.order_estimated_delivery_date, o.order_purchase_timestamp  FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN product p ON oi.product_id = p.product_id WHERE o.customer_id = %s AND order_status = %s  GROUP BY p.product_id ORDER BY o.order_purchase_timestamp DESC"""
        cursor.execute(sql, (customer_id, status))

    orders_record = cursor.fetchall()
    orders_dict = {}
    for row in orders_record:
        order_id = row[0]
        customer_id = row[1]
        order_timestamp = row[2]
        product_id = row[3]
        quantity = row[4]
        product_name = row[5]
        product_price = row[6]
        product_description = row[7]
        shipping_address = row[8]
        shipping_postal_code = row[9]
        order_status = row[10]
        order_estimate_delivery = row[11]
        order_purchase_date = row[12]


        if order_id not in orders_dict:
            orders_dict[order_id] = {
                "order_id": order_id,
                "customer_id": customer_id,
                "timestamp": order_timestamp,
                "status":order_status,
                "shipping_address":shipping_address,
                "shipping_postal_code":shipping_postal_code,
                "order_estimate_delivery":order_estimate_delivery,
                "order_purchase_date":order_purchase_date,
                "items": []
            }

        orders_dict[order_id]["items"].append({
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": product_price,
            "description":product_description
        })

    # Convert to list of orders
    orders = list(orders_dict.values())
    print(orders)

        # page configuration
    page_size = 9
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = int(request.args.get('page', 1))

    # display products can be shown per page
    order_paged ,pagination = paginate_list(orders,page,page_size,search)
    sql_db.close()

    return render_template('Customer/customer_order.html', status=status,orders=order_paged, pagination= pagination)


# id: orderID
@customer_bp.route('/customer_cancel_order/<string:order_id>', methods =['POST','GET'])
def customer_cancel_order(order_id):
    # TODO: Implement SQL statement to cancel Customer order
    if session.get("customer_id") is None:
        return redirect(url_for("auth.login"))

    cancel_reason = request.form.get('cancel_reason', '').strip()
    if not cancel_reason:
        flash("Cancellation reason is required.", "warning")
        return redirect(url_for('Customer.customer_order', status='all'))  # or current status
    sql_db = database.get_sql_db()
    sql = """
         UPDATE orders
         SET order_status = %s, order_cancellation_reason = %s
         WHERE order_id = %s
     """
    cursor = sql_db.cursor()
    params = ('Cancelled', cancel_reason, order_id)
    cursor.execute(sql, params)
    sql_db.commit()

    flash(f"Order {order_id} cancelled successfully.", "success")
    return redirect(url_for('Customer.customer_order', status='all'))  # redirect as needed


# /updateProfile/1 to access webpage for now
@customer_bp.route('/update_profile',methods=['POST','GET'])
def update_profile():

    # TODO: Implement user who logs in to be able to update their profile


    customer_id = session.get("customer_id")
    if customer_id is None:
        return redirect(url_for("auth.login"))

    db = database.get_sql_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
    row = cursor.fetchone()
    customer = Customer(*row)
    return render_template('Customer/update_profile.html' ,customer= customer)






@customer_bp.route('/customer_add_order',methods=['POST','GET'])
def customer_add_order():
    # TODO: Implement add to Customer's order with SQL statement
    selected_items = session.get("selected_items_for_checkout")
    if not session.get("customer_id") or not selected_items:
        return redirect(url_for("index"))

    order_id = "O" + str(uuid.uuid4())
    customer_id = session["customer_id"]
    order_status = "Processing"

    payment_type = request.form.get("payment_type", "Credit Card")
    payment_value = float(request.form.get("payment_value", 0))
    shipping_address = request.form.get("shipping_address")
    shipping_postal_code = request.form.get("shipping_postal_code")
    city = request.form.get("city")
    state = request.form.get("state")

    selected_ids = [item['product_id'] for item in selected_items]

    now = datetime.now()
    estimated_delivery = now + timedelta(days=10)

    mongo_db = database.get_mongo_db()
    cart_collection = mongo_db["cart"]

    sql_order = """INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, 
                order_delivery_carrier_date, order_delivery_customer_date, order_estimated_delivery_date, order_cancellation_reason, shipping_address, shipping_postal_code, city, state) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (order_id, customer_id, order_status, now, now, None, None, estimated_delivery,None,shipping_address,shipping_postal_code, city,state)

    sql_payment = """INSERT INTO payment (order_id, payment_type, payment_value) VALUES (%s, %s, %s)"""
    values_payment = (order_id, payment_type, payment_value)

    sql_order_items  =  "INSERT INTO order_items (order_id, order_item_id ,product_id, seller_id, shipping_limit_date, price, freight_value) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    now = datetime.now()
    shipping_limit_date = now + timedelta(days=3)

    db = database.get_sql_db()

    cursor = db.cursor()

    cursor.execute(sql_order, values)
    print("do")
    cursor.execute(sql_payment, values_payment)

    for item in selected_items:
        order_item_id = 1
        product_id = item["product_id"]
        quantity = item["quantity"]

        cursor.execute("SELECT price FROM product WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        price = result[0]

        for i in range(int(quantity)):
            values_order_items = (order_id,order_item_id, product_id, "S10001", shipping_limit_date, price, 0.0)
            cursor.execute(sql_order_items,values_order_items)
            order_item_id +=1


    session.pop("selected_items_for_checkout", None)
    cart_collection.update_one({"customer_id": customer_id}, {"$pull": {"items": {"product_id": {"$in": selected_ids}}}})
    db.commit()
    db.close()
    return jsonify({"message": "Order created", "order_id": order_id})




@customer_bp.route('/add_to_cart/<string:product_id>', methods=['POST','GET'])
def add_to_cart(product_id):
    customer_id = session.get("customer_id")
    if not customer_id:
        return redirect(url_for("auth.login"))

    cart = get_cart(customer_id)
    print(cart)

    for item in cart["items"]:
        if item.get("product_id") == product_id:
            item["quantity"] += 1
            break
    else:
        cart["items"].append({"product_id": product_id, "quantity": 1})

    save_cart(cart)
    return redirect(request.referrer)

@customer_bp.route('/bulk_cart_action', methods=['POST'])
def bulk_cart_action():
    action = request.form.get('action')
    selected_items = request.form.getlist('selected_items')

    if not selected_items:
        return jsonify(success=False, error="No items selected")
    cart = get_cart(session.get("customer_id"))
    if action == 'update':
        for i in range(len(selected_items)):
            product_id = selected_items[i]
            quantity_key = f"quantity_{product_id}"
            quantity = request.form.get(quantity_key,1)
            for item in cart['items']:
                if item['product_id'] == product_id:

                    item['quantity'] = int(quantity)
                    break


    elif action == 'delete':
        cart['items'] = [item for item in cart['items'] if item['product_id'] not in selected_items]
    elif action == "checkout":
        selected_data = []
        for product_id in selected_items:
            quantity = int(request.form.get(f"quantity_{product_id}", 1))
            selected_data.append({ "product_id": product_id, "quantity": quantity})
        session["selected_items_for_checkout"] = selected_data
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="Invalid action")

    save_cart(cart)
    return jsonify(success=True)



@customer_bp.route('/customer_change_password')
def customer_change_password():
    # TODO: Implement user who logged in to be able to access this page
    if session.get("customer_id") != None:
        return render_template('Customer/change_password.html')

    return redirect(url_for("auth.login"))

@customer_bp.route("/create_review/<string:product_id>", methods=["POST"])
def handle_review(product_id):
    if session.get("customer_id") is None:
        return jsonify({"message":"Please login"}), 400

    print(product_id)
    #check that the customer has an order for that product (query order_items)
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()
    cursor.execute("SELECT orders.order_id "
                   "FROM orders JOIN order_items ON orders.order_id = "
                   "order_items.order_id WHERE order_items.product_id = %s AND "
                   "orders.customer_id = %s GROUP BY orders.customer_id, "
                   "orders.order_id", (product_id,session["customer_id"]))

    customer_order_id = [row[0] for row in cursor.fetchall()]
    print(customer_order_id)
    # check if the customer already reviewed for the orders
    mongo_db = database.get_mongo_db()
    review_collection = mongo_db["reviews"]
    query = {"order_id": {"$in":customer_order_id}}
    order_id_review = list(review_collection.find(query))
    review_orders = [doc["order_id"] for doc in order_id_review]
    to_review_orders = set(customer_order_id) - set(review_orders)
    if not to_review_orders:
        return jsonify({"message":"Already reviewed"}), 400

    # Create Review
    data = request.json
    review_doc = {
        "review_id": "R" + str(uuid.uuid4()),
        "order_id": list(to_review_orders)[0],
        "review_score": int(data.get("rating")),
        "review_title": data.get("review_title"),
        "review_message": data.get("review_message"),
        "creation_date": datetime.now(),
        "product_id":product_id
    }
    mongo_db["reviews"].insert_one(review_doc)
    return jsonify({"message": "Review submitted successfully"}), 201




@customer_bp.route("/review/delete/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    mongo_db = database.get_mongo_db()
    review_collection = mongo_db["reviews"]

    result = review_collection.delete_one({"review_id": review_id})

    if result.deleted_count == 1:
        return jsonify({"message": "Review deleted successfully"}), 200
    return jsonify({"message": "Review not found"}), 404

@customer_bp.route("/review/edit/<string:review_id>", methods=["POST"])
def edit_review(review_id):
    mongo_db = database.get_mongo_db()
    review_collection = mongo_db["reviews"]

    data = request.get_json()  # get JSON data from request
    rating = data.get("rating")
    review_title = data.get("review_title")
    review_message = data.get("review_message")

    update_data = {
        "review_title": review_title,
        "review_message": review_message,
        "review_score": int(rating)
    }

    result = review_collection.update_one(
        {"review_id": review_id},
        {"$set": update_data}
    )

    if result.matched_count == 1:
        return jsonify({"message": "Review updated successfully"}), 200
    else:
        return jsonify({"message": "Review not found"}), 404


@customer_bp.route('/customer_reviews/<string:product_id>')
def customer_reviews(product_id):
    query = request.args.get("sort_by")

    mongo_db = database.get_mongo_db()
    review_collection = mongo_db["reviews"]
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    # Fetch all reviews associating with the product
    if query != "all" and query is not None:
        reviews = list(review_collection.find({"product_id": product_id,"review_score":int(query)}))
    else:
        reviews = list(review_collection.find({"product_id":product_id}))

    if not reviews:
        return render_template("customer/customer_review.html", reviews=reviews, product_id = product_id)

    #Fetch associated customer
    order_ids = [doc["order_id"] for doc in reviews]
    placeholders = ','.join(['%s'] * len(order_ids))
    sql = f"SELECT orders.order_id, customer.username, customer.photo, customer.customer_id FROM orders,customer WHERE orders.customer_id = customer.customer_id AND orders.order_id IN ({placeholders})"
    cursor.execute(sql, order_ids)
    results = cursor.fetchall()
    orderid_username = {row[0]: {"username": row[1], "profile_image": row[2], "customer_id":row[3]} for row in results}
    sql_db.close()
    return render_template("customer/customer_review.html", reviews=reviews, orderid_username = orderid_username, product_id = product_id)



@customer_bp.route("/handle_customer_update/<string:customer_id>",methods=["POST"])
def handle_customer_update(customer_id):
    sql_db = database.get_sql_db()

    try:
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        zip_code = request.form.get('zip_code')
        username = request.form.get('username')

        photo_file = request.files.get('photo')
        photo_filename = None
        if photo_file and photo_file.filename != '':
            photo_filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join('static/img/Upload', photo_filename))
            sql = """ UPDATE customer SET  name = %s,  email = %s, contact = %s,customer_zip_code = %s,username = %s ,photo = %s WHERE customer_id = %s"""
            params = [name, email, contact, zip_code, username, photo_filename]

        else:
            sql =""" UPDATE customer SET  name = %s,  email = %s, contact = %s,customer_zip_code = %s,username = %s WHERE customer_id = %s"""
            params = [name, email, contact, zip_code, username]

        params.append(customer_id)

        # Execute update
        cursor = sql_db.cursor()
        cursor.execute(sql, params)
        sql_db.commit()
        sql_db.close()
        return redirect(url_for("Customer.customer_profile"))
    except Exception as e:
        sql_db.rollback()
        error_message = f"An error occurred: {str(e)}"
        return render_template("Customer/customer_profile.html", error=error_message)