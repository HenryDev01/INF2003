import datetime

# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.

class Customer:

    def __init__(self, customer_id, customer_zip_code, username, password_hash, name, contact, email, photo):
        self._customer_id = customer_id
        self._customer_zip_code = customer_zip_code
        self._username = username
        self._password_hash = password_hash
        self._name = name
        self._contact = contact
        self._email = email
        self._photo = photo

    # ---------- Getters ----------
    def get_customer_id(self):
        return self._customer_id

    def get_customer_zip_code(self):
        return self._customer_zip_code

    def get_username(self):
        return self._username

    def get_password_hash(self):
        return self._password_hash

    def get_name(self):
        return self._name

    def get_contact(self):
        return self._contact

    def get_email(self):
        return self._email

    def get_address(self):
        return self._address

    def get_photo(self):
        return self._photo

    # ---------- Setters ----------
    def set_customer_id(self, value):
        self._customer_id = value

    def set_customer_zip_code(self, value):
        self._customer_zip_code = value

    def set_username(self, value):
        self._username = value

    def set_password_hash(self, value):
        self._password_hash = value

    def set_name(self, value):
        self._name = value

    def set_contact(self, value):
        self._contact = value

    def set_email(self, value):
        self._email = value

    def set_address(self, value):
        self._address = value

    def set_photo(self, value):
        self._photo = value

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






