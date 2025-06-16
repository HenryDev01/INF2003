
# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.

class Question:
    questionID = 0
    def __init__(self,userQuestion,username,useremail,usersubject):
        self.__userID = ''
        self.__questionID = 1
        self.__userQuestion = userQuestion
        self.__username = username
        self.__usersubject = usersubject
        self.__useremail = useremail
        self.__answer = ''
        self.__displayAsCommon = ''



    def get_question_id(self):
        return self.__questionID

    def set_userID(self, id):
        self.__userID = id

    def get_userID(self):
        return self.__userID

    def get_user_question(self):
        return self.__userQuestion

    def get_user_name(self):
        return self.__username

    def get_user_email(self):
        return self.__useremail

    def get_user_subject(self):
        return self.__usersubject

    def set_answer(self,answer):
        self.__answer = answer

    def get_answer(self):
        return self.__answer

    def set_display(self,display):
        self.__displayAsCommon= display

    def get_display(self):
        return self.__displayAsCommon