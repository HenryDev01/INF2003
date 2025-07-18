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
        delete_payments = """
            DELETE p FROM Payment p
            JOIN Orders o ON p.order_id = o.order_id
            WHERE o.customer_id = %s
        """
        cursor.execute(delete_payments, (id,))

        delete_order_items = """
            DELETE oi FROM Order_Items oi
            JOIN Orders o ON oi.order_id = o.order_id
            WHERE o.customer_id = %s
        """
        cursor.execute(delete_order_items, (id,))

        delete_orders = "DELETE FROM Orders WHERE customer_id = %s"
        cursor.execute(delete_orders, (id,))

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


@admin_bp.route('/admin_seller', methods = ["POST","GET"])
def admin_seller():

    id = ["194787"]
    return render_template('Admin/Seller.html',userList=json.dumps(id))

@admin_bp.route('/admin_retrieve_seller',methods = ['POST','GET'])
def admin_retrieve_seller():
    updateButton = "<button data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    deleteButton = "<button style ='margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"
    # if session.get('Role') != 'SysAD'  and session.get('Role') != 'User Administrator':
    #     updateButton = "<button style = 'cursor:not-allowed;'disabled data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    #     deleteButton = "<button disabled style ='cursor:not-allowed;margin-left:10px;padding-right:19px;' font-weight:bold;font-size:10px' id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"
    #

    # TODO: Retreive users with SQL
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor(dictionary=True)
    query = '''
        SELECT seller_id, username, seller_zip_code from Seller
    '''
    cursor.execute(query)
    sellers = cursor.fetchall()
    cursor.close()
    for seller in sellers:
        seller['Actions'] = updateButton + deleteButton
    return jsonify(data=sellers)
    #obj = {"adminID":194787,"fname":"Henry","lname":"Boey","role":"Ad","password":"Test",'permission':"Test","Actions":updateButton + deleteButton}
    #userList = [obj]

    #return jsonify({"data":userList})

@admin_bp.route('/admin_add_seller',methods = ['POST','GET'])
def admin_add_seller():

    username = request.form.get('username')
    zipcode = request.form.get('zipcode')
    password = request.form.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    id = str(uuid.uuid4())
    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()
    insert_query = '''
        INSERT INTO seller (
            seller_id, username,
            seller_zip_code, password_hash
        ) VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        id, username,
        zipcode, hashed_password.decode('utf-8')
    ))

    sql_db.commit()
    cursor.close()  
    return render_template("Admin/seller.html")

@admin_bp.route('/admin_update_seller', methods=["POST", "GET"])
def admin_update_seller():
    # Get form data
    sellerid = request.form.get('sellerID')
    zipcode = request.form.get('zipcode')

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        update_query = '''
            UPDATE Seller
            SET
                seller_zip_code = %s
            WHERE seller_id = %s
        '''
        cursor.execute(update_query, (zipcode, sellerid))
        sql_db.commit()
    except Exception as e:
        sql_db.rollback()
        flash(f"Error updating customer: {str(e)}", "error")
    finally:
        cursor.close()

    return render_template("Admin/seller.html")

@admin_bp.route('/admin_delete_seller' , methods = ["POST","GET"])
def admin_delete_seller():
    id = request.form.get('sellerID')
    print(id)
    if not id:
        return jsonify({"error": "Missing seller ID"}), 400

    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        delete_order_items_direct = "DELETE FROM order_items WHERE seller_id = %s"
        cursor.execute(delete_order_items_direct, (id,))

        delete_order_items_by_product = """
            DELETE FROM order_items
            WHERE product_id IN (
                SELECT product_id FROM product WHERE seller_id = %s
            )
        """
        cursor.execute(delete_order_items_by_product, (id,))
        delete_products = "DELETE FROM product WHERE seller_id = %s"
        cursor.execute(delete_products, (id,))
        delete_seller = "DELETE FROM seller WHERE seller_id = %s"
        cursor.execute(delete_seller, (id,))

        sql_db.commit()
        return jsonify({"success": True, "seller_id": id})

    except Exception as e:
        sql_db.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()


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






