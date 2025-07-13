from flask import Blueprint, render_template, jsonify, request, redirect, url_for, json, session
from App.Models.Order import Order
from App.Models import Deliverys
from App.Utils.helper import paginate_list
from App.Utils import database
admin_bp = Blueprint('Admin',__name__)
import uuid
import bcrypt
@admin_bp.route('/admindashboard')
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

    return render_template("Admin/dashboard.html")


@admin_bp.route('/customer')
def admin_customer():

    return render_template('Admin/customer.html')

@admin_bp.route('/admin_retrieve_client', methods=['GET', 'POST'])
def admin_retrieve_client():
    # TODO: Retrieve with SQL

    updateButton = "<button data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    deleteButton = "<button style ='margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"
    # if session.get('Role') != 'SysAD' and session.get('Role') != 'User Administrator':
    #     updateButton = "<button disabled data-toggle = 'modal' data-target = '#updateModal' style = 'cursor:not-allowed' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    #     deleteButton = "<button disabled style ='cursor:not-allowed;margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"
    

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor(dictionary=True)
    query = '''
        SELECT customer_id, photo, username, name, contact, email, customer_zip_code from Customer
    '''
    cursor.execute(query)
    customers = cursor.fetchall()
    cursor.close()
    for customer in customers:
        customer['photo'] = f"""
            <img src="{customer['photo']}" onerror="this.onerror=null;this.src='../static/img/Upload/default.jpg';" width="100" height="100" id="productImages" alt="Product Image">
        """
        customer['Actions'] = updateButton + deleteButton
    return jsonify(data=customers)
    
    #data = []
   # obj =   obj = {"ID":1,"nric":"T","fname":"Henry","lname":"Boey","contact":96279135,"email":"henryboey15@gmail.com","password":323232,"Actions":updateButton + deleteButton,'date':"30/03/2000",'lastPurchase':"m"}
   # data.append(obj)
    #return jsonify({"data":data})

@admin_bp.route('/admin_add_client' , methods = ["POST","GET"])
def admin_add_client():

    username = request.form.get('username')
    name = request.form.get('name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    zipcode = request.form.get('zipcode')
    password = request.form.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    id = str(uuid.uuid4())
    photo = 'default.jpg'
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()
    insert_query = '''
        INSERT INTO customer (
            customer_id, name, username, contact,
            email, customer_zip_code, photo,
            password_hash
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        id, name, username, contact,
        email, zipcode, photo,
        hashed_password.decode('utf-8')
    ))

    sql_db.commit()
    cursor.close()  
    return render_template("Admin/customer.html")


@admin_bp.route('/admin_delete_client' , methods = ["POST","GET"])
def admin_delete_client():
    id = request.form.get('id')
    print(id)
    if not id:
        return jsonify({"error": "Missing customer ID"}), 400

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        # Delete payments for customer's orders
        delete_payments = """
            DELETE p FROM Payment p
            JOIN Orders o ON p.order_id = o.order_id
            WHERE o.customer_id = %s
        """
        cursor.execute(delete_payments, (id,))

        # Delete order items for customer's orders
        delete_order_items = """
            DELETE oi FROM Order_Items oi
            JOIN Orders o ON oi.order_id = o.order_id
            WHERE o.customer_id = %s
        """
        cursor.execute(delete_order_items, (id,))

        # Delete orders for the customer
        delete_orders = "DELETE FROM Orders WHERE customer_id = %s"
        cursor.execute(delete_orders, (id,))

        # Finally, delete the customer
        delete_customer = "DELETE FROM Customer WHERE customer_id = %s"
        cursor.execute(delete_customer, (id,))

        sql_db.commit()
        return jsonify({"success": True, "customer_id": id})

    except Exception as e:
        sql_db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()


@admin_bp.route('/admin_update_client', methods=["POST", "GET"])
def admin_update_client():
    # Get form data
    username = request.form.get('username')
    name = request.form.get('name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    zipcode = request.form.get('zipcode')

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        update_query = '''
            UPDATE Customer
            SET
                name = %s,
                contact = %s,
                email = %s,
                customer_zip_code = %s
            WHERE username = %s
        '''
        cursor.execute(update_query, (name, contact, email, zipcode, username))
        sql_db.commit()
    except Exception as e:
        sql_db.rollback()
        flash(f"Error updating customer: {str(e)}", "error")
    finally:
        cursor.close()

    return render_template("Admin/customer.html")


@admin_bp.route('/inventory')
def inventory():
    # TODO: Implement user who logged in correctly to be able to view this view.
    # if session.get('adminID') != None:
    #     return render_template('inventory.html")
    # else:
    #     return redirect(url_for('index'))

    return render_template("Seller/inventory.html")



@admin_bp.route('/retrieve_inventory_product', methods = ['GET'])
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
            <img src="{product['product_photo']}" onerror="this.onerror=null;this.src='../static/img/Upload/default.jpg';" width="100" height="100" id="productImages" alt="Product Image">
        """
        product['Actions'] = updateButton + deleteButton
    return jsonify(data=products)

@admin_bp.route('/delete_inventory_product', methods = ['POST'])
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

@admin_bp.route('/add_inventory_product', methods = ['POST'])
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

@admin_bp.route('/update_inventory_product', methods = ['POST'])
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




@admin_bp.route('/Orders/<string:id>', methods=['POST','GET'])
def Orders(id):
    # TODO: Retrieve orders from SQL statement to display

    page_size = 9
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = int(request.args.get('page', 1))

    # Create 4 dummy data
    o1 = Order("Singapore", "10 Tampines Ave", "529000", "Credit Card", "4111111111111111", "123", "12/25", "12/25")
    o1.set_order_status = "Pending"
    o2 = Order("Malaysia", "22 Jalan Kuching", "51200", "Debit Card", "4222222222222222", "321", "11/26", "11/26")
    o2.set_order_status = "Cancelled"
    o3 = Order("Singapore", "5 Orchard Road", "238800", "PayPal", "N/A", "N/A", "N/A", "N/A")
    o3.set_order_status = "Delivered"
    o4 = Order("USA", "123 Main Street", "90210", "Credit Card", "4333333333333333", "456", "10/27", "10/27")
    o4.set_order_status = "Pending"

    orders = [o1, o2, o3, o4]
    pending_orders = [o for o in orders if o.get_order_status == "Pending"]
    cancelled_orders = [o for o in orders if o.get_order_status == "Cancelled"]
    delivered_orders = [o for o in orders if o.get_order_status == "Delivered"]

    all_orders, all_pagination = paginate_list(orders,page,page_size,search)
    pending_orders, pending_pagination = paginate_list(pending_orders, page, page_size, search)
    cancelled_orders, cancelled_pagination = paginate_list(cancelled_orders, page, page_size, search)
    delivered_orders, delivered_pagination = paginate_list(delivered_orders, page, page_size, search)




    return render_template('Seller/Orders.html',id=id,pagination1=all_pagination,pagination2=pending_pagination,pagination3=cancelled_pagination,pagination4=delivered_pagination,orderList=all_orders,pendingList=pending_orders,cancelledList=cancelled_orders,delieveredList=delivered_orders)


@admin_bp.route('/seller_cancel_order/<int:orderid>/<int:userid>/<int:deliveryid>',methods=['POST','GET'])
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





@admin_bp.route('/admin_seller', methods = ["POST","GET"])
def admin_seller():

    id = ["194787"]
    return render_template('Seller/Seller.html',userList=json.dumps(id))

@admin_bp.route('/retrieve_seller',methods = ['POST','GET'])
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

@admin_bp.route('/add_seller',methods = ['POST','GET'])
def add_seller():

    id = "194787M"
    return jsonify({"data":id})


@admin_bp.route('/deleteAdmin',methods = ['POST','GET'])
def delete_seller():
    # TODO: Delete with SQL
    adminID = request.form['adminID']
    return jsonify(adminID)

@admin_bp.route('/updateAdmin',  methods = ['POST','GET'])
def update_seller():

    # TODO: Update With SQL Statement
    adminID = request.form['adminID']
    return jsonify({"id":adminID})


@admin_bp.route('/Delivery',methods=['POST','GET'])
def Delivery():

    # TODO: Pull from SQL Statement to display

    d1 = Deliverys.Delivery("ORD001", "Singapore", "10 Tampines Ave", "529000", "Pending")
    deliveryList = [d1]

    return render_template('Seller/Delivery.html',deliveryList=deliveryList)




@admin_bp.route('/update_delivery_status', methods=['POST','GET'])
def update_delivery_status():
    # TODO: Implement SQL logic to update delivery status

    return redirect(url_for('Delivery'))


@admin_bp.route('/delete_delivery/<int:id>',methods=['POST','GET'])
def delete_delivery(id):
    # TODO: Implement SQL logic to delete delivery

    return redirect(url_for('Delivery'))


