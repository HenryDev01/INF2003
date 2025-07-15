from flask import Blueprint, redirect, render_template, jsonify, request, session, url_for, current_app, flash
from App.Utils import database
from App.Utils.helper import hash_password,verify_password
import uuid


auth_bp = Blueprint("auth",__name__)

@auth_bp.route('/reset_password',methods=['POST','GET'])
def reset_password():
    customer_id = session.get("customer_id")
    if not customer_id:
        return redirect(url_for("auth.login"))
    if request.method == 'GET':
        return render_template("Customer/reset_password.html")  # Render the form page

     # POST: Process password change
    print(request.form)
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")


    sql_db = database.get_sql_db()
    cursor = sql_db.cursor()

    try:
        # 1. Get current password hash from DB
        cursor.execute("SELECT password_hash FROM customer WHERE customer_id = %s", (customer_id,))
        result = cursor.fetchone()

        if not result:
            return render_template("Customer/reset_password.html", error="User not found.")

        current_hash = result[0]
        # 2. Check old password
        print(old_password)
        if not verify_password(old_password,current_hash):
            return render_template("Customer/reset_password.html", error="Old password is incorrect.")
        print("te")

        # 3. Update to new password
        new_hash = hash_password(new_password)
        cursor.execute("UPDATE customer SET password_hash = %s WHERE customer_id = %s", (new_hash, customer_id))
        sql_db.commit()


        return redirect(url_for("auth.Logout"))

    except Exception as e:
        sql_db.rollback()
        return render_template("Customer/change_password.html", error=f"Error: {str(e)}")



@auth_bp.route('/forgot_password' , methods =['POST','GET'])
def forgot_password():

    return render_template('Customer/forgot_password.html')

@auth_bp.route('/login')
def login():
    # TODO: check if user has a session such that he wont be able login again.
    # if session.get('userID') != None:
    #     print(session.get('userID'))
    #     return redirect(url_for('index'))
    # elif session.get('adminID') != None:
    #     return redirect(url_for('admin'))

    return render_template('login.html')




@auth_bp.route('/register' , methods = ["GET","POST"])
def register():
    if session.get("customer_id") is not None:
        return redirect(url_for("Product",category="Catalog"))
    return render_template('Customer/register.html',active = 'register' )

@auth_bp.route('/handle_register',methods =['POST'])
def handle_register():
    # TODO: Insert SQL statement here for register
    db = database.get_sql_db()
    data = request.get_json()
    cursor = db.cursor()
    print("dw")
    username = data.get("username")
    email = data.get("email")
    password = hash_password(data.get("password"))
    name = data.get("fname") + " " + data.get("lname")
    contact = data.get("contact")
    zip_code = data.get("zip_code")
    # address = data.get("address")
    photo = "person.jpg"
    cursor.execute("SELECT username FROM customer WHERE username = %s OR email = %s", (username,email))
    existing_customer_record = cursor.fetchone()
    if existing_customer_record:
        return jsonify({"message":"Unable to create account. An existing record is found. Please register with different email and username."}), 404

    customer_id = 'C' + str(uuid.uuid4())
    sql =  "INSERT INTO customer (customer_id,customer_zip_code,username, password_hash,name,contact,email,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (customer_id, zip_code, username,password,name,contact,email,photo)
    cursor.execute(sql,values)
    db.commit()
    db.close()

    return jsonify({'message':"Registered"})

@auth_bp.route('/handle_login' , methods = ['GET','POST'])
def handle_login():
    # TODO: Handle login for Customer and Seller using SQL statments.
    db = database.get_sql_db()
    cursor = db.cursor()

    data = request.get_json()
    # Validate empty inputs
    if not data:
        return jsonify({"message": "Missing login data"}), 400
    username = data.get("username")
    password = data.get("password")

    # Authenticate as Customer
    cursor.execute("SELECT customer_id, password_hash FROM customer WHERE username = %s", (username,))
    customer_record = cursor.fetchone()

    if customer_record and verify_password(password, customer_record[1]):
        session["customer_id"] = customer_record[0]
        db.close()
        return jsonify({"message": "customer_login_success"})

    # Authenticate as Seller
    cursor.execute("SELECT seller_id, password_hash FROM seller WHERE username = %s", (username,))
    seller_record = cursor.fetchone()

    if seller_record and verify_password(password, seller_record[1]):
        session["sellerID"] = seller_record[0]
        session["seller_logged_in"] = True
        db.close()
        return jsonify({"message": "seller_login_success"})
    # Authenticate as Admin
    cursor.execute("SELECT admin_id, password_hash FROM admin WHERE username = %s", (username,))
    admin_record = cursor.fetchone()

    if admin_record and verify_password(password, admin_record[1]):
        session["adminID"] = admin_record[0]
        session["admin_logged_in"] = True
        db.close()
        return jsonify({"message": "admin_login_success"}) 
    db.close()
    return jsonify({"message":"test"})



#checks if user logged in.
# TODO: Modified accordingly if neeeded

@auth_bp.route('/checkSession')
def checkSession():
    if session.get('customer_id') != None:
        return redirect(url_for('index'))
    elif session.get('sellerID') != None:
        return redirect(url_for('Seller.dashboard'))
    elif session.get('adminID') != None:
        return redirect(url_for('admin'))
    elif session.get('customer_id') == None:
        return redirect(url_for('auth.login'))
#    return redirect(url_for('adminLogin'))



# logout a user session
# TODO: Modified accordingly if neeeded
@auth_bp.route('/Logout')
def Logout():
     # if session.get('customer_id') != None:
     #    session.pop("customer_id")
     #    return redirect(url_for('auth.login'))
     return customer_logout()

@auth_bp.route('/sellerLogout')
def adminLogout():
    # if session.get('sellerID') != None:
    #     session['seller_logged_in'] = False
    #     session.clear()
    #     return redirect(url_for('index'))
    return seller_logout()


@auth_bp.route('/logout')
def logout():
    """Universal logout for any user type"""
    if session.get('customer_id'):
        session.pop("customer_id", None)
        flash('Customer logout successful', 'success')
    elif session.get('sellerID'):
        session.pop("sellerID", None)
        session.pop("seller_logged_in", None)
        flash('Seller logout successful', 'success')
    elif session.get('adminID'):
        session.pop("adminID", None)
        flash('Admin logout successful', 'success')

    session.clear()  # Clear everything
    return redirect(url_for('index'))

@auth_bp.route('/seller_logout')
def seller_logout():
    """Specific seller logout"""
    if session.get('sellerID'):
        session.pop("sellerID", None)
        session.pop("seller_logged_in", None)
        session.clear()
        flash('Seller logout successful', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/customer_logout')
def customer_logout():
    """Specific customer logout"""
    if session.get('customer_id'):
        session.pop("customer_id", None)
        session.clear()
        flash('Customer logout successful', 'success')
    return redirect(url_for('index'))