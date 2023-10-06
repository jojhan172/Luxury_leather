from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, fullname="", username="", postal_code="", adress="", city="", phone="") -> None:
        self.id = id
        self.email = email
        self.password = password
        self.fullname = fullname
        self.username = username
        self.postal_code = postal_code
        self.adress = adress
        self.city = city
        self.phone = phone

