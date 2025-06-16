import datetime

# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.

class User:
    countID = 0

    def __init__(self, nric, fname,lname,contact,email,password,confirmPassword):
        #instance var
        User.countID +=1
        self.__userID =  1
        self.__nric = nric
        self.__fname = fname
        self.__lname = lname
        self.__contact = contact
        self.__email = email
        self.__password = password
        self.__confirmPassword = confirmPassword
        self.__dateOfRegistration = datetime.datetime.now().date()
        self.__lastPurchase = ''
        self.__userImage = 'avatar.png'
        self.__userWishList = []
        self.__userCart = {}
        self.__userOrderList = {}
        self.__userQuantity = {}
        self.__orderID = []
        self.__newOrderID = []

    def get_userID(self):
        return self.__userID

    def set_nric(self,nric):
        self.__nric = nric

    def get_nric(self):
        return self.__nric

    def set_fname(self, fname):
        self.__fname = fname

    def get_fname(self):
        return self.__fname

    def set_lname(self, lname):
        self.__lname = lname

    def get_lname(self):
        return self.__lname

    def get_contact(self):
        return self.__contact

    def set_contact(self,contact):
        self.__contact = contact

    def set_email(self,email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_password(self,password):
        self.__password = password

    def get_password(self):
        return self.__password

    def get_confirmPassword(self):
        return self.__confirmPassword

    def get_dor(self):
        return self.__dateOfRegistration

    def set_userImage(self, image):
        self.__userImage = image

    def get_userImage(self):
        return self.__userImage

    def set_wishlist(self,item):
        self.__userWishList.append(item)

    def get_wishlist(self):
        return self.__userWishList

    def set_cart(self, item):
        self.__userCart = item

    def get_cart(self):
        return self.__userCart

    def set_last_purchase(self,lastPurchase):
        self.__lastPurchase = lastPurchase

    def get_last_purchase(self):
        return self.__lastPurchase

    def set_order(self, item):
        self.__userOrderList = item

    def get_order(self):
        return self.__userOrderList

    def set_userQuantity(self,quantity):
        self.__userQuantity = quantity

    def get_userQuantity(self):
        return self.__userQuantity

    def set_orderID(self, orderID):
        self.__orderID.append(orderID)

    def get_orderID(self):
        return self.__orderID

    def set_neworderID(self, orderID):
        self.__newOrderID.append(orderID)

    def get_neworderID(self):
        return self.__newOrderID


class Administrator:
    def __init__(self,adminID,firstName,lastName,Role,password,permission):
        self.__adminID = adminID
        self.__firstName = firstName
        self.__lastName = lastName
        self.__Role = Role
        self.__password = password
        self.__permission  = permission

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def get_firstName(self):
        return self.__firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def get_lastName(self):
        return self.__lastName

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    def set_adminID(self, adminID):
        self.__adminID = adminID

    def get_adminID(self):
        return self.__adminID

    def set_role(self,Role):
        self.__Role = Role

    def get_role(self):
        return self.__Role

    def set_permission(self, permission):
        self.__permission = permission

    def get_permission(self):
        return self.__permission




