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
    username = data.get("username")
    email = data.get("email")
    password = hash_password(data.get("password"))
    name = data.get("fname") + " " + data.get("lname")
    contact = data.get("contact")
    zip_code = data.get("zip_code")
    address = data.get("address")
    photo = "person.jpg"
    cursor.execute("SELECT username FROM customer WHERE username = %s OR email = %s", (username,email))
    existing_customer_record = cursor.fetchone()
    if existing_customer_record:
        return jsonify({"message":"Unable to create account. An existing record is found. Please register with different email and username."}), 404

    customer_id = 'C' + str(uuid.uuid4())
    sql =  "INSERT INTO customer (customer_id,customer_zip_code,username, password_hash,name,contact,email,address,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (customer_id, zip_code, username,password,name,contact,email,address,photo)
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
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT customer_id,password_hash FROM customer WHERE username = %s", (username,))
    record = cursor.fetchone()

    if not record:
        return jsonify({"message": "test"}), 404

    customer_id = record[0]
    password_hash = record[1]

    if not verify_password(password,password_hash):
        return jsonify({"message": "test"}),404

    session["customer_id"] = customer_id
    db.close()

    return jsonify({"message":"test"})



#checks if user logged in.
# TODO: Modified accordingly if neeeded

@auth_bp.route('/checkSession')
def checkSession():
    if session.get('customer_id') != None:
        return redirect(url_for('index'))
    elif session.get('adminID') != None:
        return redirect(url_for('admin'))
    elif session.get('customer_id') == None:
        return redirect(url_for('login'))
#    return redirect(url_for('adminLogin'))



# logout a user session
# TODO: Modified accordingly if neeeded
@auth_bp.route('/Logout')
def Logout():

     if session.get('customer_id') != None:
        session.pop("customer_id")
        return redirect(url_for('auth.login'))

@auth_bp.route('/sellerLogout')
def adminLogout():
    if session.get('sellerID') != None:
        session['seller_logged_in'] = False
        session.clear()
        return redirect(url_for('index'))