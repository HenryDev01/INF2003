import datetime

class Order:
    def __init__(
        self, order_id, customer_id, order_status,
        order_purchase_timestamp, order_approved_at,
        order_delivery_carrier_date, order_delivery_customer_date,
        order_estimated_delivery_date
    ):
        self.__order_id = order_id
        self.__customer_id = customer_id
        self.__order_status = order_status
        self.__order_purchase_timestamp = order_purchase_timestamp
        self.__order_approved_at = order_approved_at
        self.__order_delivery_carrier_date = order_delivery_carrier_date
        self.__order_delivery_customer_date = order_delivery_customer_date
        self.__order_estimated_delivery_date = order_estimated_delivery_date

    # Getters
    def get_order_id(self):
        return self.__order_id

    def get_customer_id(self):
        return self.__customer_id

    def get_order_status(self):
        return self.__order_status

    def get_order_purchase_timestamp(self):
        return self.__order_purchase_timestamp

    def get_order_approved_at(self):
        return self.__order_approved_at

    def get_order_delivery_carrier_date(self):
        return self.__order_delivery_carrier_date

    def get_order_delivery_customer_date(self):
        return self.__order_delivery_customer_date

    def get_order_estimated_delivery_date(self):
        return self.__order_estimated_delivery_date

    def get_orderID(self):
        """Template expects get_orderID() - maps to order_id"""
        return self.__order_id

    def get_username(self):
        """Template expects get_username() - return customer username"""
        return getattr(self, 'username', 'N/A')

    def get_orderDate(self):
        """Template expects get_orderDate() - return purchase timestamp"""
        if self.__order_purchase_timestamp:
            return self.__order_purchase_timestamp.strftime('%Y-%m-%d %H:%M')
        return 'N/A'

    def get_paymentMethod(self):
        """Template expects get_paymentMethod() - return payment type"""
        return getattr(self, 'payment_method', 'N/A')

    def get_cardNumber(self):
        """Template expects get_cardNumber() - always return N/A for security"""
        return 'N/A'

    def get_status(self):
        """Template expects get_status() - maps to order_status"""
        return self.__order_status

    def get_grandTotal(self):
        """Template expects get_grandTotal() - return calculated total"""
        return getattr(self, 'grand_total', 0.0)

    # Setters
    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_order_status(self, order_status):
        self.__order_status = order_status

    def set_order_purchase_timestamp(self, timestamp):
        self.__order_purchase_timestamp = timestamp

    def set_order_approved_at(self, approved_at):
        self.__order_approved_at = approved_at

    def set_order_delivery_carrier_date(self, carrier_date):
        self.__order_delivery_carrier_date = carrier_date

    def set_order_delivery_customer_date(self, customer_date):
        self.__order_delivery_customer_date = customer_date

    def set_order_estimated_delivery_date(self, estimated_date):
        self.__order_estimated_delivery_date = estimated_date
