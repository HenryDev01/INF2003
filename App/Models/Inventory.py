class Product:

    def __init__(self, id, product_category, product_name, product_weight_g,
                 product_length_cm, product_height_cm, product_width_cm,
                 product_photo, has_stock, product_description,
                 product_model, product_price, seller_id):
        self.__product_id = id
        self.__category = product_category
        self.__name = product_name
        self.__weight = product_weight_g
        self.__length = product_length_cm
        self.__height = product_height_cm
        self.__width = product_width_cm
        self.__photo = product_photo
        self.__stock = has_stock
        self.__description = product_description
        self.__model = product_model
        self.__price = product_price
        self.__ratings = 0
        self.__seller_id = seller_id

    # product_id
    def get_product_id(self):
        return self.__product_id

    # Category
    def set_category(self, category):
        self.__category = category

    def get_category(self):
        return self.__category

    # Photo
    def set_photo(self, url):
        self.__photo = url

    def get_photo(self):
        return self.__photo

    # Name
    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    # Description
    def set_description(self, description):
        self.__description = description

    def get_description(self):
        return self.__description

    # Stock
    def set_stock(self, stock):
        self.__stock = stock

    def get_stock(self):
        return self.__stock

    # Price
    def set_price(self, price):
        self.__price = price

    def get_price(self):
        return self.__price

    # Brand
    def set_brand(self, brand):
        self.__brand = brand

    def get_brand(self):
        return self.__brand

    # Model
    def set_model(self, model):
        self.__model = model

    def get_model(self):
        return self.__model

    # Rating
    def set_rating(self, ratings):
        self.__ratings = ratings

    def get_rating(self):
        return self.__ratings

    # Weight
    def set_weight(self, weight):
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    # Length
    def set_length(self, length):
        self.__length = length

    def get_length(self):
        return self.__length

    # Height
    def set_height(self, height):
        self.__height = height

    def get_height(self):
        return self.__height

    # Width
    def set_width(self, width):
        self.__width = width

    def get_width(self):
        return self.__width

    # Seller ID
    def get_seller_id(self):
        return self.__seller_id
