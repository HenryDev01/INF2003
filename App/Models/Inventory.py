# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.

class Products:
    productID = 0

    def __init__(self,url,name,brand,model,description,stock,price):
        Products.productID+=1
        self.__productID =1
        self.__url = url
        self.__name = name
        self.__description  = description
        self.__stock = stock
        self.__price = price
        self.__brand = brand
        self.__model = model
        self.__productDate =''


    def get_product_id(self):
        return self.__productID

    def set_url(self, url):
        self.__url = url

    def get_url(self):
        return self.__url

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_description(self, description):
        self.__description = description

    def get_description(self):
        return self.__description

    def set_stock(self, stock):
        self.__stock = stock

    def get_stock(self):
        return self.__stock

    def set_price(self, price):
        self.__price = price

    def get_price(self):
        return self.__price

    def set_brand(self,brand):
        self.__brand = brand

    def get_brand(self):
        return self.__brand

    def set_model(self,model):
        self.__model = model

    def get_model(self):
        return self.__model

    def set_productDate(self,productDate):
        self.__productDate = productDate

    def get_productDate(self):
        return self.__productDate
