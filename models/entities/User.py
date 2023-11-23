from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password) -> None:
        self.id = id
        self.email = email
        self.password = password

    @classmethod
    def editAccount(self, db, userType:str, userId:str, parameter:str, newValue:str) -> 0:
        cursor = db.cursor()
        if userType == 'seller':
            table = 'seller_users'
        else: 
            table = 'client_users' 
        sql = "UPDATE `{table}` SET `{parameter}` = '{newValue}' WHERE `{table}`.`id` = '{userId}'".format(table=table, userId= userId, parameter=parameter, newValue=newValue)
        cursor.execute(sql)
        db.commit()
        return
        
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

    @classmethod
    def takeOrderByClientId(self, db, clientId:str) -> list:
        cursor = db.cursor()
        sql = "SELECT * FROM `cart_products` WHERE `clientId` LIKE '{clientId}'".format(clientId=clientId)
        cursor.execute(sql)
        row = list(cursor.fetchall())
        return row
    
    @classmethod
    def pay_order(self, clientId) -> 0:
        return
        

class Seller(User):
    def __init__(self, id, email, password, ceoName="", companyName="", userType="") -> None:
        super().__init__(id, email, password)
        self.ceoName = ceoName
        self.companyName = companyName
        self.userType = userType

    @classmethod
    def takeSellerById(self, db, sellerId: str) -> list:
        cursor  = db.cursor()
        sql = "SELECT * FROM `seller_users` WHERE `id` Like '{}'".format(sellerId)
        cursor.execute(sql)
        row = list(cursor.fetchall())
        return row



