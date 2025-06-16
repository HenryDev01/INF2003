import datetime

# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.

class Order:

    deliveryID = 0
    orderID =0
    def __init__(self,country,address,postalCode,paymentMethod,cardNumber,CVVCode,expDate):
        Order.orderID +=1
        Order.deliveryID +=1
        self.__orderID = self.orderID
        self.__country = country
        self.__address = address
        self.__postalCode = postalCode
        self.__paymentMethod = paymentMethod
        self.__cardNumber = cardNumber
        self.__CVCode = CVVCode
        self.__expDate = expDate
        self.__userID = ''
        self.__username =''
        self.__productID =''
        self.__grandTotal =''
        self.__status = 'Pending'
        self.__orderDate = datetime.datetime.today().date()
        self.__userQuantity = {}
        self.__deliveryID = self.deliveryID


    def get_orderID(self):
        return self.__orderID


    def get_deliveryID(self):
        return self.__deliveryID


    def set_country(self,country):
        self.__country = country

    def get_country(self):
        return self.__country

    def set_address(self,address):
        self.__address = address

    def get_address(self):
        return self.__address

    def set_postalCode(self,postalCode):
        self.__postalCode = postalCode

    def get_postalCode(self):
        return self.__postalCode

    def set_paymentMethod(self, paymentMethod):
        self.__paymentMethod = paymentMethod

    def get_paymentMethod(self):
        return self.__paymentMethod

    def set_cardNumber(self, cardNumber):
        self.__cardNumber = cardNumber

    def get_cardNumber(self):
        return self.__cardNumber[0:13]

    def set_CVVCode(self, CVVCode):
        self.__CVVCode = CVVCode

    def get_CVVCode(self):
        return self.__CVVCode

    def set_expDate(self, expDate):
        self.__expDate = expDate

    def get_expDate(self):
        return self.__expDate

    def set_userID(self,ID):
        self.__userID = ID

    def get_userID(self):
        return self.__userID

    def set_username(self,username):
        self.__username = username

    def get_username(self):
        return self.__username

    def set_productID(self, ID):
        self.__productID = ID

    def get_productID(self):
        return self.__productID

    def set_grrandTotal(self, total):
        self.__grandTotal = total

    def get_grandTotal(self):
        return self.__grandTotal

    def set_status(self,status):
        self.__status = status

    def get_status(self):
        return self.__status

    def get_orderDate(self):
        return self.__orderDate

    def get_userQuantity(self):
        return self.__userQuantity