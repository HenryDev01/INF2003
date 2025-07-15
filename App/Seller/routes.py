import os

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, json, session
from App.Models.Order import Order
from App.Models import Deliverys
from App.Utils.helper import paginate_list
from App.Utils import database
from werkzeug.utils import secure_filename




from App.Utils import database
seller_bp = Blueprint('Seller',__name__)
import uuid

@seller_bp.route('/dashboard')
def dashboard():
    # seller_id = session.get("sellerID")
    # if not seller_id:
    #     return redirect(url_for("auth.login"))

    # Get chart data
    top_quantity = database.get_top_products_by_quantity("S10001")
    top_revenue = database.get_top_products_by_revenue("S10001")
    geo_labels, geo_data = database.get_top_geolocation_sales("S10001")
    cat_labels, cat_data = database.get_top_cat_by_revenue("S10001")
    print(cat_labels,cat_data)

    daily = database.get_daily_order_counts("S10001")
    monthly = database.get_monthly_order_counts("S10001")
    today_count = database.get_total_orders_today("S10001")
    this_month_count = database.get_total_orders_thisMonth("S10001")
    yearly_count = database.get_yearly_order("S10001")
    this_year_count = database.get_thisYear_order("S10001")

    monthly_sales = database.get_monthly_revenue("S10001")
    daily_sales = database.get_daily_revenue("S10001")
    today_revenue = database.get_revenue_today("S10001")
    this_month_revenue = database.get_revenue_this_month("S10001")
    yearly_revenue = database.get_yearly_revenue("S10001")
    this_year_revenue = database.get_revenue_this_year("S10001")
    monthly_average_revenue = database.get_monthly_average("S10001")

    monthly_average = database.get_monthly_average("S10001")  # Replace with get_monthly_average() if exists
    total = database.get_total_earnings("S10001")
    sales = database.get_sales_count("S10001")  # Replace with get_sales_count() if exists
    customer_count = database.get_customer_count("S10001")  # Replace with get_customer_count() if exists

    # task list
    to_pack = database.get_to_pack_count("S10001")
    pending = database.get_pending_count("S10001")
    out_of_stock = database.get_out_of_stock_count("S10001")
    pending_refund = database.get_pending_refund_count("S10001")
    cancellation_rate, refund_rate = database.get_cancellation_and_refund_rates("S10001")

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
    url = "<img src = '' width = '100px' height = '100px' id = 'productImages'>"
    updateButton = "<button data-toggle = 'modal' data-target = '#updateModal' id = 'updateBtn' class='btn btn-info ' '>Update</button>"
    deleteButton = "<button  id = 'deleteBtn' class='delbtn btn btn-danger'>Delete</button>"


    sql_db = database.get_sql_db()
    cursor = sql_db.cursor(dictionary=True)
    # replace seller_id using session
    query = '''
        SELECT * from Product WHERE seller_id = "S10001" 
    '''
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    print(products)
    for product in products:
        product['product_photo'] = f"""
            <img src="../static/img/Upload/{product['product_photo']}" onerror="this.onerror=null;this.src='../static/img/Upload/keyboard.jpg';" width="100" height="100" id="productImages" alt="Product Image">
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
            weight, length, width, height, price, "S10001"
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


