from flask import Blueprint, render_template,redirect,url_for, jsonify

customer_bp = Blueprint("Customer",__name__)

@customer_bp.route('/customer_profile')
def customer_profile():
    usersdict = {}
    # TODO: Replace this section with SQL to view their own profile for logged in users.
    # if session.get('user_logged_in') != None:

    return render_template('Customer/customer_profile.html', usersdict=usersdict)



# id : userID
#/checkout/1 to access the page for now
@customer_bp.route('/checkout/<string:id>')
def checkout(id):
    # TODO: Implement checks out by user id
    print(id)
    return render_template('Customer/checkout.html')



# <string:status> - all, pending, cancelled, delivered
# /customer_order/all to access webpage
@customer_bp.route('/customer_order/<string:status>',methods=['POST','GET'])
def customer_order(status):
    # TODO: Implement user who logged in to be able to view their own order only.
    print(status)
    return render_template('Customer/customer_order.html', status=status)

# id: orderID
@customer_bp.route('/customer_cancel_order/<int:id>', methods =['POST','GET'])
def customer_cancel_order(id):
    # TODO: Implement SQL statement to cancel Customer order
    return redirect(url_for('index'))


# /updateProfile/1 to access webpage for now
@customer_bp.route('/update_profile/<string:usernames>',methods=['POST','GET'])
def update_profile(usernames):

    # TODO: Implement user who logs in to be able to update their profile

    # if session.get('userID') !=  None:
    #
    #     return render_template('update_profile.html',usersdict=usersdict,form=form)
    # else:
    #     return redirect(url_for('login'))
    return render_template('Customer/update_profile.html')




@customer_bp.route('/customer_add_order',methods=['POST','GET'])
def customer_add_order():
    # TODO: Implement add to Customer's order with SQL statement
    return jsonify('Test')




@customer_bp.route('/add_to_cart/<int:id>', methods=['POST','GET'])
def add_to_cart(id):
    # TODO: Use SQL statement to add items to Customer's cart and display dynamically in HTML
    return redirect('/Product/Catalog')

@customer_bp.route('/delete_from_cart/<int:id>', methods=['POST','GET'])
def delete_from_cart(id):
    # TODO: USe SQL statement to delete from Customer's cart

    return redirect('/Product/Catalog')

# product id <>
@customer_bp.route('/update_from_cart/<int:id>', methods=['POST','GET'])
def update_from_cart(id):
    # TODO: Use SQL statement to update Customer's cart
    return redirect('/Product/Catalog')

@customer_bp.route('/customer_change_password')
def customer_change_password():
    # TODO: Implement user who logged in to be able to access this page

    return render_template('Customer/change_password.html')






