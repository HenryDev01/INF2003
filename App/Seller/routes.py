import os
from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, json, session, flash
from App.Models.Order import Order
from App.Models import Deliverys
from App.Utils.helper import paginate_list
from App.Utils import database
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId





from App.Utils import database
seller_bp = Blueprint('Seller',__name__)
import uuid

@seller_bp.route('/dashboard')
def dashboard():
    seller_id = session.get('sellerID')
    if not seller_id:
        flash('Please login as seller', 'error')
        return redirect(url_for('auth.login'))


    # Get chart data
    top_quantity = database.get_top_products_by_quantity(seller_id)
    top_revenue = database.get_top_products_by_revenue(seller_id)
    geo_labels, geo_data = database.get_top_geolocation_sales(seller_id)
    cat_labels, cat_data = database.get_top_cat_by_revenue(seller_id)
    print(cat_labels,cat_data)

    daily = database.get_daily_order_counts(seller_id)
    monthly = database.get_monthly_order_counts(seller_id)
    today_count = database.get_total_orders_today(seller_id)
    this_month_count = database.get_total_orders_thisMonth(seller_id)
    yearly_count = database.get_yearly_order(seller_id)
    this_year_count = database.get_thisYear_order(seller_id)

    monthly_sales = database.get_monthly_revenue(seller_id)
    daily_sales = database.get_daily_revenue(seller_id)
    today_revenue = database.get_revenue_today(seller_id)
    this_month_revenue = database.get_revenue_this_month(seller_id)
    yearly_revenue = database.get_yearly_revenue(seller_id)
    this_year_revenue = database.get_revenue_this_year(seller_id)
    monthly_average_revenue = database.get_monthly_average(seller_id)

    monthly_average = database.get_monthly_average(seller_id)  # Replace with get_monthly_average() if exists
    total = database.get_total_earnings(seller_id)
    sales = database.get_sales_count(seller_id)  # Replace with get_sales_count() if exists
    customer_count = database.get_customer_count(seller_id)  # Replace with get_customer_count() if exists

    # task list
    to_pack = database.get_to_pack_count(seller_id)
    pending = database.get_pending_count(seller_id)
    out_of_stock = database.get_out_of_stock_count(seller_id)
    pending_refund = database.get_pending_refund_count(seller_id)
    cancellation_rate, refund_rate = database.get_cancellation_and_refund_rates(seller_id)

    daily_serializable = [
        {'day': r['day'].isoformat(), 'total_orders': r['total_orders']}
        for r in daily
    ]
    return render_template("Seller/dashboard.html",
        topQuantityLabels=[r['product_name'] for r in top_quantity],
        topQuantityData=[r['total_quantity'] for r in top_quantity],
        topRevenueLabels=[r['product_name'] for r in top_revenue],
        topRevenueData=[r['total_revenue'] for r in top_revenue],
        topGeolocationLabels=geo_labels,
        topGeolocationData=geo_data,
        topCategoryLabels=cat_labels,
        topCategoryData=cat_data,
        monthly_average=monthly_average,
        total=total,
        sales=sales,
        customer_count=customer_count,
       daily_count=daily_serializable,
       monthly_count=monthly,
       today_count=today_count,
       this_month_count=this_month_count,
       yearly_count=yearly_count,
       this_year_count=this_year_count,
        monthly_sales = monthly_sales,
        daily_sales = daily_sales,
        today_revenue = today_revenue,
        this_month_revenue = this_month_revenue,
        yearly_revenue = yearly_revenue,
        this_year_revenue = this_year_revenue,
        monthly_average_revenue = monthly_average_revenue,
       to_pack=to_pack,
       pending=pending,
       out_of_stock=out_of_stock,
       pending_refund=pending_refund,
       cancellation_rate=cancellation_rate,
       refund_rate=refund_rate

    )


@seller_bp.route("/Refunds/<status>")
def refunds(status):
    db = database.get_sql_db()
    cursor = db.cursor()

    if status == "all":
        cursor.execute("""
            SELECT order_id, customer_id, order_purchase_timestamp, order_status, 
                   order_delivery_customer_date, order_cancellation_reason, 
                   shipping_address, shipping_postal_code, city, state
            FROM orders
            WHERE order_status LIKE 'Refund%'
        """)
    else:
        cursor.execute("""
            SELECT order_id, customer_id, order_purchase_timestamp, order_status, 
                   order_delivery_customer_date, order_cancellation_reason, 
                   shipping_address, shipping_postal_code, city, state
            FROM orders
            WHERE order_status = %s
        """, (status,))

    rows = cursor.fetchall()

    refundList = []
    for row in rows:
        refundList.append({
            "order_id": row[0],
            "customer_id": row[1],
            "order_purchase_timestamp": row[2],
            "order_status": row[3],
            "order_delivery_customer_date": row[4],
            "order_cancellation_reason": row[5],
            "shipping_address": row[6],
            "shipping_postal_code": row[7],
            "city": row[8],
            "state": row[9],
        })

    db.close()

    return render_template("Seller/refunds.html", refundList=refundList, id=status)


@seller_bp.route("/update_refund_status/<order_id>", methods=["POST"])
def update_refund_status(order_id):
    new_status = request.form.get("status")

    db = database.get_sql_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE orders
        SET order_status = %s
        WHERE order_id = %s
    """, (new_status, order_id))

    db.commit()
    db.close()

    return redirect(url_for("Seller.refunds", status="all"))


@seller_bp.route('/client')
def seller_client():

    return render_template('Seller/client.html')

@seller_bp.route('/seller_retrieve_client', methods=['GET', 'POST'])
def seller_retrieve_client():
    # TODO: Retrieve with SQL

    updateButton = "<button data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    deleteButton = "<button style ='margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"
    # if session.get('Role') != 'SysAD' and session.get('Role') != 'User Administrator':
    #     updateButton = "<button disabled data-toggle = 'modal' data-target = '#updateModal' style = 'cursor:not-allowed' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    #     deleteButton = "<button disabled style ='cursor:not-allowed;margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"

    data = []
    obj =   obj = {"ID":1,"nric":"T","fname":"Henry","lname":"Boey","contact":96279135,"email":"henryboey15@gmail.com","password":323232,"Actions":updateButton + deleteButton,'date':"30/03/2000",'lastPurchase':"m"}
    data.append(obj)
    return jsonify({"data":data})

@seller_bp.route('/seller_add_client' , methods = ["POST","GET"])
def seller_add_client():

    #  TODO: Use SQL Statement to add

    obj = {"ID": 194787, "nric": 1, "fname": 1, "lname": 1,
               "contact": 1, "email": 1, "password": 1,
               "Actions": "<button data-toggle='modal' data-target='#updateModal' id = 'updateBtn' class='btn btn-primary ' '>Update</button><button style ='margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='btn btn-danger'>Delete</button>"}
    data = [obj]
    return jsonify({"data": data})



@seller_bp.route('/seller_delete_client' , methods = ["POST","GET"])
def seller_delete_client():
    # TODO: Implement SQL statement to delete users.
    return jsonify({"id":id})

@seller_bp.route('/seller_update_client',methods=["POST","GET"])
def seller_update_client():
    # TODO: Update using SQL statement
    return jsonify({"id":id})


@seller_bp.route('/inventory')
def inventory():
    # TODO: Implement user who logged in correctly to be able to view this view.
    # if session.get('adminID') != None:
    #     return render_template('inventory.html")
    # else:
    #     return redirect(url_for('index'))

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor(dictionary=True)
    cursor.execute("SELECT product_category_translation FROM category_translation")
    results = cursor.fetchall()
    print(results)

    return render_template("Seller/inventory.html",categories =results)



@seller_bp.route('/retrieve_inventory_product', methods = ['GET'])
def retrieve_inventory_product():
    seller_id = session.get('sellerID')
    if not seller_id:
        return jsonify(data=[])

    url = "<img src = '' width = '100px' height = '100px' id = 'productImages'>"
    updateButton = "<button data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    deleteButton = "<button  id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor(dictionary=True)
    query = '''
        SELECT * from Product WHERE seller_id = %s
    '''
    cursor.execute(query, (seller_id,))
    products = cursor.fetchall()
    cursor.close()
    for product in products:
        product['product_photo'] = f"""
            <img src="../static/img/Upload/{product['product_photo']}" onerror="this.onerror=null;this.src='../static/img/Upload/keyboard.jpg';" width="100" height="100" id="productImages" alt="Product Image">
        """
        product['Actions'] = updateButton + deleteButton
    return jsonify(data=products)

@seller_bp.route('/delete_inventory_product', methods = ['POST'])
def delete_inventory_product():
    seller_id = session.get('sellerID')
    if not seller_id:
        return jsonify({"error": "Please login as seller"}), 401

    id = request.form['id'].strip()
    if not id:
        return jsonify({"error": "Missing product ID"}), 400
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        cursor.execute("SELECT seller_id FROM Product WHERE product_id = %s", (id,))
        result = cursor.fetchone()

        if not result or result[0] != seller_id:
            return jsonify({"error": "Product not found or you are not authorized to delete it"}), 403

        delete_query1 = "DELETE FROM Order_Items WHERE product_id = %s"
        delete_query2 = "DELETE FROM Product WHERE product_id = %s AND seller_id = %s"

        cursor.execute(delete_query1, (id,))
        cursor.execute(delete_query2, (id, seller_id))
        sql_db.commit()
        return jsonify({"success": True, "id": id})
    except Exception as e:
        sql_db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@seller_bp.route('/add_inventory_product', methods = ['POST'])
def add_inventory_product():
    seller_id = session.get('sellerID')
    if not seller_id:
        flash('Please login as seller first', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        category = request.form.get('category')
        name = request.form.get('name')
        brand = request.form.get('brand')
        model = request.form.get('model')
        description = request.form.get('description')
        stock = 1 if request.form.get('stock') == '1' else 0
        price = request.form.get('price')
        url = request.form.get('url')
        weight = request.form.get('weight')
        length = request.form.get('length')
        width = request.form.get('width')
        height = request.form.get('height')

        # Handle file upload
        file = request.files.get('image')

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(os.getcwd(), 'static', 'img', 'upload')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))


        id = str(uuid.uuid4())
        sql_db = database.get_sql_db()
        cursor = sql_db.cursor()

        insert_query = '''
                    INSERT INTO product (
                        product_id, product_category_translation, product_name, product_model,
                        product_description, has_stock, product_photo,
                        product_weight_g, product_length_cm, product_width_cm, product_height_cm, price, seller_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
        cursor.execute(insert_query, (
            id, category, name, model,
            description, stock, filename,
            weight, length, width, height, price, seller_id
        ))

        sql_db.commit()
        cursor.close()


    return redirect(url_for('Seller.inventory'))

@seller_bp.route('/update_inventory_product', methods = ['POST'])
def update_inventory_product():
    seller_id = session.get('sellerID')
    if not seller_id:
        flash('Please login as seller first', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        category = request.form.get('updateCategory')
        name = request.form.get('updateName')
        model = request.form.get('updateModel')
        current_filename = request.form.get("currentFileName")
        description = request.form.get('updateDescription')
        stock = 1 if request.form.get('updateStock') == '1' else 0
        price = request.form.get('updatePrice')
        file = request.files.get('updateUrl')
        weight = request.form.get('updateWeight')
        length = request.form.get('updateLength')
        width = request.form.get('updateWidth')
        height = request.form.get('updateHeight')
        id = request.form.get('productID')
        sql_db = database.get_sql_db()
        cursor = sql_db.cursor()

        if file and file.filename != '':

            url= secure_filename(file.filename)
            upload_folder = os.path.join(os.getcwd(), 'static', 'img', 'upload')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, url))

        else:
            url = current_filename

        update_query = '''
            UPDATE Product
            SET
                product_category_translation = %s,
                product_name = %s,
                product_model = %s,
                product_description = %s,
                has_stock = %s,
                product_photo = %s,
                product_weight_g = %s,
                product_length_cm = %s,
                product_width_cm = %s,
                product_height_cm = %s,
                price = %s
            WHERE product_id = %s AND seller_id = %s
        '''
        try:
            cursor.execute(update_query, (
                category, name, model, description, stock, url, weight, length, width, height, price, id, seller_id
            ))

            if cursor.rowcount == 0:
                flash('Product not found or you are not authorized to update it', 'error')
            else:
                flash('Product updated successfully!', 'success')

            sql_db.commit()
        except Exception as e:
            sql_db.rollback()
            flash(f'Error updating product: {str(e)}', 'error')
        finally:
            cursor.close()

    return redirect(url_for('Seller.inventory'))

@seller_bp.route('/Orders/<string:id>', methods=['POST','GET'])
def Orders(id):
    # TODO: Retrieve orders from SQL statement to display
    seller_id = session.get('sellerID')
    if not seller_id:
        flash('Please login as seller', 'error')
        return redirect(url_for('auth.login'))

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    # Base query for all orders
    base_query = """
        SELECT DISTINCT o.order_id, 
                o.customer_id, 
                o.order_purchase_timestamp,
                o.order_status, 
                o.shipping_address, 
                o.shipping_postal_code,
                c.username, 
                p.payment_value, 
                p.payment_type,
                o.order_estimated_delivery_date
        FROM Orders o
        JOIN Customer c ON o.customer_id = c.customer_id
        JOIN Payment p ON o.order_id = p.order_id
        JOIN Order_Items oi ON o.order_id = oi.order_id
        WHERE oi.seller_id = %s
    """

    if id == 'processing':
        query = base_query + " AND o.order_status = 'Processing' ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))
    elif id == 'cancelled':
        query = base_query + " AND o.order_status = 'Cancelled' ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))
    elif id == 'delivered':
        query = base_query + " AND o.order_status = 'Delivered' ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))
    elif id == 'shipped':
        query = base_query + " AND o.order_status = 'Shipped' ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))
    elif id == 'packed':
        query = base_query + " AND o.order_status = 'Packed' ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))
    else:
        query = base_query + " ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))

    orders_data = cursor.fetchall()
    print(orders_data)

    # Get order items for each order
    orders_with_items = []
    for order_row in orders_data:
        order_id = order_row[0]

        # Get items for this order
        items_query = """
            SELECT oi.product_id,
                    p.product_name,
                    p.product_description,
                    COUNT(oi.order_item_id) as quantity,
                    oi.price
            FROM Order_Items oi
            JOIN Product p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s AND oi.seller_id = %s
            GROUP BY oi.product_id
        """
        cursor.execute(items_query, (order_id, seller_id))
        items = cursor.fetchall()

        order_obj = Order(
            order_id=order_row[0],
            customer_id=order_row[1],
            order_status=order_row[3],
            order_purchase_timestamp=order_row[2],
            order_approved_at=None,
            order_delivery_carrier_date=None,
            order_delivery_customer_date=None,
            order_estimated_delivery_date=order_row[9]
        )

        # Set additional attributes
        order_obj.username = order_row[6]
        order_obj.payment_method = order_row[8]
        order_obj.payment_value = order_row[7]
        order_obj.shipping_address = order_row[4]
        order_obj.shipping_postal_code = order_row[5]
        order_obj.items = items

        grand_total = sum(item[4] * item[3] for item in items)  # price * quantity
        order_obj.grand_total = grand_total

        orders_with_items.append(order_obj)

    page_size = 9
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = int(request.args.get('page', 1))

    paginated_orders, pagination = paginate_list(orders_with_items, page, page_size, False)

    template_data = {'id': id}
    if id == 'all':
        template_data.update({'pagination1': pagination, 'orderList': paginated_orders})
    elif id == 'processing':
        template_data.update({'pagination2': pagination, 'processingList': paginated_orders})
    elif id == 'shipped':
        template_data.update({'pagination3': pagination, 'shippedList': paginated_orders})
    elif id == 'cancelled':
        template_data.update({'pagination4': pagination, 'cancelledList': paginated_orders})
    elif id == 'delivered':
        template_data.update({'pagination5': pagination, 'deliveredList': paginated_orders})
    elif id == "packed":
        template_data.update({'pagination6': pagination, 'packedList': paginated_orders})

    print(template_data)
    sql_db.close()
    return render_template('Seller/Orders.html', **template_data)





@seller_bp.route('/seller_cancel_order/<int:orderid>/<int:userid>/<int:deliveryid>',methods=['POST','GET'])
def seller_cancel_order(orderid,userid,deliveryid):

    #TODO: Implement SQL logic to cancel order. Remove delivery and order from Customer.

    # if int(orderid) in userOrder:
    #     userOrder[int(orderid)].set_status('Cancelled')
    # userOrderID.remove(int(orderid))
    #
    # ordersDict[orderid].set_status('Cancelled')
    #
    # deliverysDict[int(orderid)].set_status('Cancelled')



    return redirect('/Orders/all')


@seller_bp.route('/update_order_status/<string:order_id>', methods=['POST'])
def update_order_status(order_id):
    seller_id = session.get('sellerID')
    if not seller_id:
        flash('Please login as seller', 'error')
        return redirect(url_for('auth.login'))

    new_status = request.form.get('status')

    # Validate status
    valid_statuses = ['Processing', 'Shipped', 'Delivered', 'Cancelled', 'Packed']
    if new_status not in valid_statuses:
        flash('Invalid status', 'error')
        return redirect(request.referrer or url_for('Seller.Orders', id='all'))

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        # Verify seller has items in this order
        cursor.execute("""
                       SELECT COUNT(*)
                       FROM order_items
                       WHERE order_id = %s
                         AND seller_id = %s
                       """, (order_id, seller_id))

        if cursor.fetchone()[0] == 0:
            flash('You are not authorized to update this order', 'error')
            return redirect(request.referrer or url_for('Seller.Orders', id='all'))

        # Get current status for validation
        cursor.execute("SELECT order_status FROM Orders WHERE order_id = %s", (order_id,))
        result = cursor.fetchone()
        if not result:
            flash('Order not found', 'error')
            return redirect(request.referrer)

        current_status = result[0]

        valid_transitions = {
            'Processing': ['Packed', 'Cancelled'],
            'Packed':['Shipped', 'Cancelled'],
            'Shipped': ['Delivered'],  # Can't cancel after shipped
            'Delivered': [],
            'Cancelled': []
        }

        if new_status not in valid_transitions.get(current_status, []):
            flash(f'Cannot change status from {current_status} to {new_status}', 'error')
            return redirect(request.referrer)

        # Update order status with timestamps
        now = datetime.now()
        if new_status == 'Shipped':
            cursor.execute("""
                           UPDATE Orders
                           SET order_status = %s, order_delivery_carrier_date = %s
                           WHERE order_id = %s
                           """, (new_status, now, order_id))
        elif new_status == "Packed":
            cursor.execute("""
                           UPDATE Orders
                           SET order_status = %s, order_delivery_carrier_date = %s
                           WHERE order_id = %s
                                       """, (new_status, now, order_id))
        elif new_status == 'Delivered':
            cursor.execute("""
                           UPDATE Orders
                           SET order_status = %s, order_delivery_customer_date = %s
                           WHERE order_id = %s
                           """, (new_status, now, order_id))
        else:
            cursor.execute("""
                           UPDATE Orders
                           SET order_status = %s
                           WHERE order_id = %s
                           """, (new_status, order_id))

        sql_db.commit()
        flash(f'Order {order_id} updated to {new_status}', 'success')

    except Exception as e:
        sql_db.rollback()
        flash(f'Error updating order: {str(e)}', 'error')
    finally:
        sql_db.close()

    return redirect(request.referrer or url_for('Seller.Orders', id='all'))

@seller_bp.route('/order_details/<string:order_id>')
def order_details(order_id):
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    # Fetch complete order details including all items
    query = """
            SELECT o.order_id, \
                   o.customer_id, \
                   o.order_status, \
                   o.order_purchase_timestamp,
                   o.order_estimated_delivery_date, \
                   o.shipping_address, \
                   o.shipping_postal_code,
                   o.city, \
                   o.state, \
                   c.username, \
                   c.email, \
                   c.contact,
                   oi.product_id, \
                   p.product_name, \
                   p.product_description,
                   COUNT(oi.order_item_id) as quantity, \
                   oi.price,
                   pay.payment_type, \
                   pay.payment_value
            FROM orders o
                     JOIN customer c ON o.customer_id = c.customer_id
                     JOIN order_items oi ON o.order_id = oi.order_id
                     JOIN product p ON oi.product_id = p.product_id
                     JOIN payment pay ON o.order_id = pay.order_id
            WHERE o.order_id = %s
            GROUP BY oi.product_id \
            """

    cursor.execute(query, (order_id,))
    results = cursor.fetchall()

    if not results:
        sql_db.close()
        return render_template('error.html', message="Order not found"), 404

    # Process results - organize data structure
    order_info = {
        'order_id': results[0][0],
        'customer_id': results[0][1],
        'order_status': results[0][2],
        'order_date': results[0][3],
        'estimated_delivery': results[0][4],
        'shipping_address': results[0][5],
        'shipping_postal_code': results[0][6],
        'city': results[0][7],
        'state': results[0][8],
        'customer_username': results[0][9],
        'customer_email': results[0][10],
        'customer_contact': results[0][11],
        'payment_type': results[0][17],
        'payment_value': results[0][18],
        'items': []
    }

    # Process each order item
    total_amount = 0
    for row in results:
        item = {
            'product_id': row[12],
            'product_name': row[13],
            'product_description': row[14],
            'quantity': row[15],
            'unit_price': row[16],
            'line_total': row[15] * row[16]  # quantity * price
        }
        order_info['items'].append(item)
        total_amount += item['line_total']

    order_info['total_amount'] = total_amount

    sql_db.close()

    # Render template with order details
    return render_template('Seller/order_details.html', order=order_info)

@seller_bp.route('/seller', methods = ["POST","GET"])
def seller():

    id = ["194787"]
    return render_template('Seller/Seller.html',userList=json.dumps(id))

@seller_bp.route('/retrieve_seller',methods = ['POST','GET'])
def retrieve_seller():
    updateButton = "<button data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    deleteButton = "<button style ='margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"
    # if session.get('Role') != 'SysAD'  and session.get('Role') != 'User Administrator':
    #     updateButton = "<button style = 'cursor:not-allowed;'disabled data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    #     deleteButton = "<button disabled style ='cursor:not-allowed;margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"
    #

    # TODO: Retreive users with SQL

    obj = {"adminID":194787,"fname":"Henry","lname":"Boey","role":"Ad","password":"Test",'permission':"Test","Actions":updateButton + deleteButton}
    userList = [obj]

    return jsonify({"data":userList})

@seller_bp.route('/add_seller',methods = ['POST','GET'])
def add_seller():

    id = "194787M"
    return jsonify({"data":id})


@seller_bp.route('/deleteAdmin',methods = ['POST','GET'])
def delete_seller():
    # TODO: Delete with SQL
    adminID = request.form['adminID']
    return jsonify(adminID)

@seller_bp.route('/updateAdmin',  methods = ['POST','GET'])
def update_seller():

    # TODO: Update With SQL Statement
    adminID = request.form['adminID']
    return jsonify({"id":adminID})


@seller_bp.route('/Delivery',methods=['POST','GET'])
def Delivery():

    # TODO: Pull from SQL Statement to display

    d1 = Deliverys.Delivery("ORD001", "Singapore", "10 Tampines Ave", "529000", "Processing")
    deliveryList = [d1]

    return render_template('Seller/Delivery.html',deliveryList=deliveryList)


@seller_bp.route('/update_delivery_status', methods=['POST','GET'])
def update_delivery_status():
    # TODO: Implement SQL logic to update delivery status

    return redirect(url_for('Delivery'))


@seller_bp.route('/delete_delivery/<int:id>',methods=['POST','GET'])
def delete_delivery(id):
    # TODO: Implement SQL logic to delete delivery

    return redirect(url_for('Delivery'))

@seller_bp.route('/debug_session')
def debug_session():
    """Debug route to check session contents"""
    return jsonify({
        'session_keys': list(session.keys()),
        'sellerID': session.get('sellerID'),
        'seller_logged_in': session.get('seller_logged_in'),
        'customer_id': session.get('customer_id'),
        'all_session': dict(session)
    })


@seller_bp.route('/debug_orders/<string:id>')
def debug_orders(id):
    """Debug route to see what data is being returned"""
    seller_id = session.get('sellerID', 'S001')

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    base_query = """
                 SELECT DISTINCT o.order_id,
                                 o.customer_id,
                                 o.order_purchase_timestamp,
                                 o.order_status,
                                 o.shipping_address,
                                 o.shipping_postal_code,
                                 c.username,
                                 p.payment_value,
                                 p.payment_type,
                                 o.order_estimated_delivery_date
                 FROM Orders o
                          JOIN Customer c ON o.customer_id = c.customer_id
                          JOIN Payment p ON o.order_id = p.order_id
                          JOIN Order_Items oi ON o.order_id = oi.order_id
                 WHERE oi.seller_id = %s \
                 """

    if id == 'processing':
        query = base_query + " AND o.order_status = 'Processing' ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))
    else:
        query = base_query + " ORDER BY o.order_purchase_timestamp DESC"
        cursor.execute(query, (seller_id,))

    orders_data = cursor.fetchall()

    # Return raw data as JSON for debugging
    debug_info = {
        'seller_id': seller_id,
        'query_used': query,
        'orders_count': len(orders_data),
        'orders_raw_data': [list(row) for row in orders_data],  # Convert to list for JSON
    }

    # Also try to create Order objects like your main route
    if orders_data:
        sample_order = orders_data[0]
        debug_info['sample_order_fields'] = {
            'order_id': sample_order[0],
            'customer_id': sample_order[1],
            'order_purchase_timestamp': str(sample_order[2]),
            'order_status': sample_order[3],
            'username': sample_order[6],
            'payment_value': sample_order[7],
            'payment_type': sample_order[8]
        }

        from App.Models.Order import Order
        order_obj = Order(
            order_id=sample_order[0],
            customer_id=sample_order[1],
            order_status=sample_order[3],
            order_purchase_timestamp=sample_order[2],
            order_approved_at=None,
            order_delivery_carrier_date=None,
            order_delivery_customer_date=None,
            order_estimated_delivery_date=sample_order[9]
        )

        # Set additional attributes
        order_obj.username = sample_order[6]
        order_obj.payment_method = sample_order[8]
        order_obj.payment_value = sample_order[7]
        order_obj.grand_total = float(sample_order[7])  # Use payment_value as grand total for now

        # Test the methods
        debug_info['order_object_methods'] = {
            'get_orderID()': order_obj.get_orderID(),
            'get_username()': order_obj.get_username(),
            'get_orderDate()': order_obj.get_orderDate(),
            'get_paymentMethod()': order_obj.get_paymentMethod(),
            'get_status()': order_obj.get_status(),
            'get_grandTotal()': order_obj.get_grandTotal()
        }

    sql_db.close()

    return jsonify(debug_info)


@seller_bp.route('/debug_orders_simple/<string:id>')
def debug_orders_simple(id):
    """Simple debug without Order object creation"""
    seller_id = session.get('sellerID', 'S001')

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    base_query = """
                 SELECT DISTINCT o.order_id,
                                 o.customer_id,
                                 o.order_purchase_timestamp,
                                 o.order_status,
                                 o.shipping_address,
                                 o.shipping_postal_code,
                                 c.username,
                                 p.payment_value,
                                 p.payment_type,
                                 o.order_estimated_delivery_date
                 FROM Orders o
                          JOIN Customer c ON o.customer_id = c.customer_id
                          JOIN Payment p ON o.order_id = p.order_id
                          JOIN Order_Items oi ON o.order_id = oi.order_id
                 WHERE oi.seller_id = %s
                 ORDER BY o.order_purchase_timestamp DESC \
                 """

    cursor.execute(base_query, (seller_id,))
    orders_data = cursor.fetchall()

    debug_info = {
        'seller_id_from_session': session.get('sellerID'),
        'seller_id_used': seller_id,
        'orders_found': len(orders_data),
        'session_contents': dict(session),
    }

    if orders_data:
        debug_info['sample_order'] = {
            'order_id': orders_data[0][0],
            'customer_id': orders_data[0][1],
            'order_date': str(orders_data[0][2]),
            'order_status': orders_data[0][3],
            'customer_username': orders_data[0][6],
            'payment_value': orders_data[0][7],
        }

        debug_info['all_orders'] = []
        for order in orders_data:
            debug_info['all_orders'].append({
                'order_id': order[0],
                'status': order[3],
                'customer': order[6],
                'amount': order[7]
            })

    sql_db.close()
    return jsonify(debug_info)


@seller_bp.route('/reviews')
def seller_reviews():
    seller_id = session.get('sellerID')
    if not seller_id:
        flash('Please login as seller', 'error')
        return redirect(url_for('auth.login'))

    # get reviews from Mongo
    mongo_db = database.get_mongo_db()
    collection = mongo_db["reviews"]
    seller_product_ids = get_seller_product_ids(seller_id)
    reviews = list(collection.find({"product_id": {"$in": seller_product_ids}}))

    # get order_ids from those reviews
    order_ids = [
        review["order_id"]
        for review in reviews
        if "order_id" in review
    ]

    if order_ids:
        # connect to SQL
        db = database.get_sql_db()
        cursor = db.cursor(dictionary=True)

        # fetch orders → customer_id
        placeholders = ', '.join(['%s'] * len(order_ids))
        sql = f"""
            SELECT order_id, customer_id
            FROM orders
            WHERE order_id IN ({placeholders})
        """
        cursor.execute(sql, order_ids)
        orders_result = cursor.fetchall()

        order_to_customer_id = {
            row["order_id"]: row["customer_id"]
            for row in orders_result
        }

        customer_ids = list(set(order_to_customer_id.values()))

        customer_map = {}
        if customer_ids:
            placeholders = ', '.join(['%s'] * len(customer_ids))
            sql = f"""
                SELECT customer_id, username
                FROM customer
                WHERE customer_id IN ({placeholders})
            """
            cursor.execute(sql, customer_ids)
            customers_result = cursor.fetchall()

            customer_map = {
                row["customer_id"]: row["username"]
                for row in customers_result
            }

        # attach customer name to reviews
        for review in reviews:
            order_id = review.get("order_id")
            customer_id = order_to_customer_id.get(order_id)
            customer_name = customer_map.get(customer_id, "Unknown") if customer_id else "Unknown"
            review["customer_name"] = customer_name

        cursor.close()
        db.close()
    else:
        # no orders
        for review in reviews:
            review["customer_name"] = "Unknown"

    return render_template('Seller/order_review.html', reviews=reviews)

@seller_bp.route('/seller/bulk_reply_reviews', methods=['POST'])
def bulk_reply_reviews():
    mongo_db = database.get_mongo_db()
    collection = mongo_db["reviews"]

    # Grab all hidden inputs for review IDs
    review_ids = request.form.getlist('review_id_list')

    for review_id in review_ids:
        reply_field_name = f"reply_message_{review_id}"
        reply_message = request.form.get(reply_field_name)

        if reply_message is not None:
            collection.update_one(
                {"review_id": review_id},
                {"$set": {"seller_reply": reply_message}}
            )

    flash("Replies saved successfully.", "success")
    return redirect(request.referrer)




def get_seller_product_ids(seller_id):
    query = "SELECT product_id FROM product WHERE seller_id = %s"
    db = database.get_sql_db()
    cursor = db.cursor()
    cursor.execute(query, (seller_id,))
    rows = cursor.fetchall()
    # rows is a list of tuples, extract product_id values
    product_ids = [row[0] for row in rows]
    return product_ids