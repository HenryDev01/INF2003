class Review:
    def __init__(self, review_id, order_id, review_score, review_title, review_message, review_creation_date):
        self.__review_id = review_id
        self.__order_id = order_id
        self.__review_score = review_score
        self.__review_title = review_title
        self.__review_message = review_message
        self.__review_creation_date = review_creation_date

    # Getters
    def get_review_id(self):
        return self.__review_id

    def get_order_id(self):
        return self.__order_id

    def get_review_score(self):
        return self.__review_score

    def get_review_title(self):
        return self.__review_title

    def get_review_message(self):
        return self.__review_message

    def get_review_creation_date(self):
        return self.__review_creation_date

    # Setters
    def set_review_id(self, review_id):
        self.__review_id = review_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_review_score(self, review_score):
        self.__review_score = review_score

    def set_review_title(self, review_title):
        self.__review_title = review_title

    def set_review_message(self, review_message):
        self.__review_message = review_message

    def set_review_creation_date(self, review_creation_date):
        self.__review_creation_date = review_creation_date