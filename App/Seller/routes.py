from flask import Blueprint, render_template, jsonify, request, redirect, url_for, json, session, flash
from App.Models.Order import Order
from App.Models import Deliverys
from App.Utils.helper import paginate_list
from App.Utils import database
seller_bp = Blueprint('Seller',__name__)
import uuid

@seller_bp.route('/dashboard')
def dashboard():
    # TODO: replace with SQL logic to access to dashboard for correct users
    # if session.get('adminID') != None:
    #     print(session.get('firstName'))
    #     salesDict ={}
    #     db = shelve.open('storage.db','c')
    #     try:
    #         salesDict = db['Sales']
    #     except:
    #         print('gdrgdg')
    #
    #     total = 0
    #     for key in salesDict:
    #         total+=salesDict[key]
    #     db.close()
    #     print(salesDict)
    #     return render_template('dashboard.html',salesDict=salesDict,total=total)
    # else:
    #     return redirect(url_for("login"))
    seller_id = session.get("sellerID")
    if seller_id is None:
        return redirect(url_for("auth.login"))

    return render_template("Seller/dashboard.html")


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

    return render_template("Seller/inventory.html")



@seller_bp.route('/retrieve_inventory_product', methods = ['GET'])
def retrieve_inventory_product():
    url = "<img src = '' width = '100px' height = '100px' id = 'productImages'>"
    updateButton = "<button data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    deleteButton = "<button  id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"


    sql_db = database.get_sql_db()
    cursor = sql_db.cursor(dictionary=True)
    query = '''
        SELECT * from Product
    '''
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    for product in products:
        product['product_photo'] = f"""
            <img src="{product['product_photo']}" onerror="this.onerror=null;this.src='../static/img/Upload/keyboard.jpg';" width="100" height="100" id="productImages" alt="Product Image">
        """
        product['Actions'] = updateButton + deleteButton
    return jsonify(data=products)

@seller_bp.route('/delete_inventory_product', methods = ['POST'])
def delete_inventory_product():
    id = request.form['id'].strip()
    if not id:
        return jsonify({"error": "Missing product ID"}), 400
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        delete_query1 = "DELETE FROM Order_items WHERE product_id = %s"
        delete_query2 = "DELETE FROM product WHERE product_id = %s"
        cursor.execute(delete_query1, (id,))
        cursor.execute(delete_query2, (id,))
        sql_db.commit()
        return jsonify({"success": True, "id": id})
    except Exception as e:
        sql_db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@seller_bp.route('/add_inventory_product', methods = ['POST'])
def add_inventory_product():
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
        id = str(uuid.uuid4())
        sql_db = database.get_sql_db()
        cursor = sql_db.cursor()
        insert_query = '''
            INSERT INTO product (
                product_id, product_category_translation, product_name, product_model,
                product_description, has_stock, product_photo,
                product_weight_g, product_length_cm, product_width_cm, product_height_cm, price
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (
            id, category, name, model,
            description, stock, url,
            weight, length, width, height, price
        ))

        sql_db.commit()
        cursor.close()

    
    return redirect(url_for('Seller.inventory'))

@seller_bp.route('/update_inventory_product', methods = ['POST'])
def update_inventory_product():
    if request.method == 'POST':
        category = request.form.get('updateCategory')  
        name = request.form.get('updateName')  
        model = request.form.get('updateModel')
        description = request.form.get('updateDescription')
        stock = 1 if request.form.get('updateStock') == '1' else 0
        price = request.form.get('updatePrice')
        url = request.form.get('updateUrl')
        weight = request.form.get('updateWeight')
        length = request.form.get('updateLength')
        width = request.form.get('updateWidth')
        height = request.form.get('updateHeight')
        id = request.form.get('productID')
        sql_db = database.get_sql_db()
        cursor = sql_db.cursor()
        update_query = '''
            UPDATE product
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
            WHERE product_id = %s
        '''
        cursor.execute(update_query, (
            category, name, model, description, stock, url, weight, length, width, height, price, id  
        ))


        sql_db.commit()
        cursor.close()

    
    return redirect(url_for('Seller.inventory'))




@seller_bp.route('/Orders/<string:id>', methods=['POST','GET'])
def Orders(id):
    # TODO: Retrieve orders from SQL statement to display
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    # Base query for all orders
    base_query = """
                 SELECT o.order_id, \
                        o.customer_id, \
                        o.order_purchase_timestamp,
                        o.order_status, \
                        o.shipping_address, \
                        o.shipping_postal_code,
                        c.username, \
                        p.payment_value, \
                        p.payment_type
                        o.order_estimated_delivery_date
                 FROM orders o
                          JOIN customer c ON o.customer_id = c.customer_id
                          JOIN payment p ON o.order_id = p.order_id \
                 """

    if id == 'pending':
        cursor.execute(base_query + " WHERE o.order_status = 'Processing'")
    elif id == 'cancelled':
        cursor.execute(base_query + " WHERE o.order_status = 'Cancelled'")
    elif id == 'delivered':
        cursor.execute(base_query + " WHERE o.order_status = 'Delivered'")
    else:
        cursor.execute(base_query + " ORDER BY o.order_purchase_timestamp DESC")

    orders_data = cursor.fetchall()

    # Get order items for each order
    orders_with_items = []
    for order_row in orders_data:
        order_id = order_row[0]

        # Get items for this order
        items_query = """
                      SELECT oi.product_id, \
                             p.product_name, \
                             p.product_description,
                             COUNT(oi.order_item_id) as quantity, \
                             oi.price
                      FROM order_items oi
                               JOIN product p ON oi.product_id = p.product_id
                      WHERE oi.order_id = %s
                      GROUP BY oi.product_id \
                      """
        cursor.execute(items_query, (order_id,))
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
        order_obj.items = items
        orders_with_items.append(order_obj)

    page_size = 9
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = int(request.args.get('page', 1))

    if id == 'all':
        paginated_orders, pagination = paginate_list(orders_with_items, page, page_size, search)
        return render_template('Seller/Orders.html', id=id, pagination1=pagination, orderList=paginated_orders)
    elif id == 'pending':
        paginated_orders, pagination = paginate_list(orders_with_items, page, page_size, search)
        return render_template('Seller/Orders.html', id=id, pagination2=pagination, pendingList=paginated_orders)
    elif id == 'cancelled':
        paginated_orders, pagination = paginate_list(orders_with_items, page, page_size, search)
        return render_template('Seller/Orders.html', id=id, pagination3=pagination, cancelledList=paginated_orders)
    elif id == 'delivered':
        paginated_orders, pagination = paginate_list(orders_with_items, page, page_size, search)
        return render_template('Seller/Orders.html', id=id, pagination4=pagination, deliveredList=paginated_orders)

    sql_db.close()

    # # Create 4 dummy data
    # o1 = Order("Singapore", "10 Tampines Ave", "529000", "Credit Card", "4111111111111111", "123", "12/25", "12/25")
    # o1.set_order_status = "Pending"
    # o2 = Order("Malaysia", "22 Jalan Kuching", "51200", "Debit Card", "4222222222222222", "321", "11/26", "11/26")
    # o2.set_order_status = "Cancelled"
    # o3 = Order("Singapore", "5 Orchard Road", "238800", "PayPal", "N/A", "N/A", "N/A", "N/A")
    # o3.set_order_status = "Delivered"
    # o4 = Order("USA", "123 Main Street", "90210", "Credit Card", "4333333333333333", "456", "10/27", "10/27")
    # o4.set_order_status = "Pending"
    #
    # orders = [o1, o2, o3, o4]
    # pending_orders = [o for o in orders if o.get_order_status == "Pending"]
    # cancelled_orders = [o for o in orders if o.get_order_status == "Cancelled"]
    # delivered_orders = [o for o in orders if o.get_order_status == "Delivered"]
    #
    # all_orders, all_pagination = paginate_list(orders,page,page_size,search)
    # pending_orders, pending_pagination = paginate_list(pending_orders, page, page_size, search)
    # cancelled_orders, cancelled_pagination = paginate_list(cancelled_orders, page, page_size, search)
    # delivered_orders, delivered_pagination = paginate_list(delivered_orders, page, page_size, search)
    #
    # return render_template('Seller/Orders.html',id=id,pagination1=all_pagination,pagination2=pending_pagination,pagination3=cancelled_pagination,pagination4=delivered_pagination,orderList=all_orders,pendingList=pending_orders,cancelledList=cancelled_orders,delieveredList=delivered_orders)


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
    new_status = request.form.get('status')

    # Validate status
    valid_statuses = ['Processing', 'Shipped', 'Delivered', 'Cancelled']
    if new_status not in valid_statuses:
        flash('Invalid status', 'error')
        return redirect(request.referrer or url_for('Seller.Orders', id='all'))

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        cursor.execute("UPDATE orders SET order_status = %s WHERE order_id = %s",
                       (new_status, order_id))
        sql_db.commit()
        flash(f'Order {order_id} updated to {new_status}', 'success')
    except Exception as e:
        sql_db.rollback()
        flash(f'Error updating order: {str(e)}', 'error')
    finally:
        sql_db.close()

    # Redirect back to the same orders page
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

    d1 = Deliverys.Delivery("ORD001", "Singapore", "10 Tampines Ave", "529000", "Pending")
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


