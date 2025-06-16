from flask import Flask,render_template,request
from flask_wtf import CSRFProtect
from flask_mail import Mail, Message
from App.config import Config
from App.Models.ContactForm import  ContactForm
from App.Models import Inventory, Users
from App.Models.Question import Question
from Utils.helper import paginate_list
from Utils import database
from Seller.routes import seller_bp
from Auth.routes import auth_bp
from Customer.routes import customer_bp


app = Flask(__name__,template_folder='template')
app.config.from_object(Config)
app.register_blueprint(seller_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(auth_bp)

csrf = CSRFProtect(app)
csrf.init_app(app)
mail = Mail()
mail.init_app(app)

#SQL EXAMPLE:
# db  =database.get_sql_db()  # configure your sql db credential in get_sql_db() under Utils/database.py. Use mariaDB credential
# cursor = db.cursor()
# cursor.execute("SELECT * FROM STUDENT")
# data = cursor.fetchone()
# user = Users.User(data[3],data[3],data[3],data[3],data[3],data[3],data[3])
# print(user.get_nric())
# db.close()

#NOSQL
#db =database.get_mongo_db()  # configure your mongodb in get_mongo_db().


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    # TODO: Check if user has logged in with SQL
    # if session.get('userID') != None:
    #     usersDict = {}
    #     db = shelve.open("storage.db", 'c')
    #     try:
    #         usersDict = db['User']
    #     except:
    #         print("Unable to retrieve")
    #
    #     userorder = usersDict[session['userID']].get_order()
    #     #userorder.pop(2)
    #     userCart = usersDict[session['userID']].get_cart()
    #     print(userCart)
    #     print(productList)
    #     #db['User'] = usersDict
    #     print(userorder)
    #     return render_template('index.html',productList=productList,userCart = userCart,counts =len(userCart),today=today)
    # else:

    return render_template('Customer/index.html')


@app.route('/Product/<string:category>')
def Product(category):
    # TODO: Remove this Dummy Data and pull from sql instead
    p1 = Inventory.Products(
        "keyboard.jpg",
        "Mechanical Gaming Keyboard",
        "Logitech",
        "G512",
        "RGB mechanical keyboard with tactile switches and customizable lighting.",
        15,
        129.90
    )

    page_size = 9
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = int(request.args.get('page', 1))


    productList = []
    productList.append(p1)


    # display products can be shown per page
    offset = (page - 1) * page_size
    List1 = productList[offset:offset + 9]
    pagination = paginate_list(productList,page,page_size,search)

    return render_template('Customer/shop.html' , active = 'Product', pagination=pagination, category=category, count=len(productList), productsList=List1)






#
@app.route('/support', methods=['POST', 'GET'])
def support():

    form = ContactForm()
    if request.method == "POST":
        send_message({"message":form.message.data})
    q1 = Question("How long does shipping usually take?","test","test","test")
    q1.set_display("Yes")
    q1.set_answer("Shipping typically takes 3-7 business days for standard delivery. Expedited options are available at checkout for faster delivery.")

    q2 = Question("How long does it takes to deliver to the Customer?","test","test","test")
    q2.set_display("Yes")
    q2.set_answer("This depends on whether the product is in stock. In the situation where product is out of stock we may contact you to change or refund.")

    questionList = []
    questionList.append(q1)
    questionList.append(q2)

    return render_template('Customer/support.html', active ='Contact',form=form,questionList=questionList )

def send_message(message):
    print(message.get('name'))

    msg = Message(message.get('subject'), sender=message.get('email'),
                  recipients=['pietoncharm@gmail.com'],
                  body=message.get('message')
                  )
    mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True)

