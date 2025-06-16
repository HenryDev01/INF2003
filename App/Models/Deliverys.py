# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.

import datetime

class Delivery:
    def __init__(self,orderID,country,address,postalCode,status):
        self.__deliveryID = orderID
        self.__orderID = orderID
        self.__country = country
        self.__address =address
        self.__productID =''
        self.__userID =''
        self.__username = ''
        self.__postalCode =postalCode
        self.__estimateDate = datetime.date.today()
        self.__status =status



    def get_deliveryID(self):
        return self.__deliveryID

    def set_country(self, country):
        self.__country = country

    def get_country(self):
        return self.__country

    def set_address(self, address):
        self.__address = address

    def get_address(self):
        return self.__address

    def set_postalCode(self, postalCode):
        self.__postalCode = postalCode

    def get_postalCode(self):
        return self.__postalCode

    def get_orderID(self):
        return self.__orderID

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username

    def set_productID(self, ID):
        self.__productID = ID

    def get_productID(self):
        return self.__productID

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

    def get_estimateDate(self):
        return self.__estimateDate + datetime.timedelta(days=3)

    def set_userID(self, ID):
        self.__userID = ID

    def get_userID(self):
        return self.__userID
