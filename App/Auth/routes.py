from flask import Blueprint, redirect, render_template, jsonify, request, session,url_for
from App.Models.ContactForm import ForgotForm

auth_bp = Blueprint("auth",__name__)


@auth_bp.route('/reset_password',methods=['POST','GET'])
def reset_password():

    # TODO: Implement SQL statements to reset password
    return redirect('/login')




@auth_bp.route('/forgot_password' , methods =['POST','GET'])
def forgot_password():
    # TODO: Implement SQL logic for forgot password.
    form = ForgotForm()
    return render_template('Customer/forgot_password.html',form= form)






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

    return render_template('Customer/register.html',active = 'register' )

@auth_bp.route('/handle_register',methods =['POST'])
def handle_register():
    # TODO: Insert SQL statement here for register

    message = "Registered"
    return jsonify({'message':message})

@auth_bp.route('/handle_login' , methods = ['GET','POST'])
def handle_login():
    # TODO: Handle login for Customer and Seller using SQL statments.

    username = request.form['username']
    password = request.form['password']

    return jsonify({'username':username,'password':password})



#checks if user logged in.
# TODO: Modified accordingly if neeeded

@auth_bp.route('/checkSession')
def checkSession():
    if session.get('userID') != None:
        return redirect(url_for('index'))
    elif session.get('adminID') != None:
        return redirect(url_for('admin'))
    elif session.get('userID') == None:
        return redirect(url_for('login'))
#    return redirect(url_for('adminLogin'))



# logout a user session
# TODO: Modified accordingly if neeeded
@auth_bp.route('/Logout')
def Logout():

     if session.get('customerID') != None:
        session['customer_logged_in'] = False
        session.clear()
        return redirect(url_for('login'))

@auth_bp.route('/sellerLogout')
def adminLogout():
    if session.get('sellerID') != None:
        session['seller_logged_in'] = False
        session.clear()
        return redirect(url_for('index'))