# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.

class Cart:
    def __init__(self,itemName,quantity,price):
        self.__itemName = itemName
        self.__quantity = quantity
        self.__total = quantity*price
        self.__grandTotal = ''

    def set_item_name(self,item):
        self.__itemName = item

    def get_item_name(self):
        return self.__itemName

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_quantity(self):
        return self.__quantity


    def set_total(self, price,quantity):
        self.__total = price*quantity

    def get_total(self):
        return self.__total

    def set_grand_total(self,grandTotal):
        self.__grandTotal = grandTotal

    def get_grand_total(self):
        return self.__grandTotal