from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password) -> None:
        self.id = id
        self.email = email
        self.password = password
        
class Client(User):
    def __init__(self, id, email, password, fullname="", username="", postal_code="", adress="", city="", phone="", userType="") -> None:
        super().__init__(id, email, password)
        self.fullname = fullname
        self.username = username
        self.postal_code = postal_code
        self.adress = adress
        self.city = city
        self.phone = phone
        self.userType = userType
        

class Seller(User):
    def __init__(self, id, email, password, ceoName="", companyName="", usertype="") -> None:
        super().__init__(id, email, password)
        self.ceoName = ceoName
        self.companyName = companyName
        self.userType = usertype



