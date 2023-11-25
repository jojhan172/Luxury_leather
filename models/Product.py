import uuid

class Product():
    def __init__(self, id, name, price, sellerId, imgURL) -> None:
        self.id = id
        self.price = price
        self.name = name
        self.imgURL = imgURL
        self.sellerId = sellerId
    
    def addToDb(self, db): # Añade un nuevo producto con los datos que el vendedor proporcione a traves del formulario
        try:
            cursor = db.cursor()
            sql = "INSERT INTO `products` (`id`, `name`, `price`, `sellerId`, `imgURL`) VALUES ('{id}', '{name}', '{price}', '{sellerId}', '{imgURL}')".format(id= self.id, name = self.name, price=self.price, sellerId = self.sellerId, imgURL = self.imgURL)
            cursor.execute(sql)
            db.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def takeProducts(self, db) -> list:
        cursor = db.cursor()
        sql = "SELECT * FROM `products`"
        cursor.execute(sql)
        row = list(cursor.fetchall())
        return row
    
    @classmethod
    def takeProductsWithLimit(self, db, limit:int) -> list:
        cursor = db.cursor()
        sql = "SELECT * FROM `products` LIMIT {}".format(limit)
        cursor.execute(sql)
        row = list(cursor.fetchall())
        return row
    
    @classmethod
    def takeProductsBySeller(self, db, sellerId: str)-> list:
        cursor = db.cursor() 
        sql = "SELECT * FROM `products` WHERE `sellerId` LIKE '{}'".format(sellerId)
        cursor.execute(sql)
        row = list(cursor.fetchall())
        return row

    @classmethod
    def takeProductsById(self, db, productId) -> list:
        cursor = db.cursor() 
        sql = "SELECT * FROM `products` WHERE `id` LIKE '{}'".format(productId)
        cursor.execute(sql)
        row = (cursor.fetchall())
        return row

    @classmethod
    def editProduct(self, db, productId:str, parameter:str, newValue:str) -> 0:
        cursor = db.cursor()
        sql= "UPDATE `products` SET `{parameter}` = '{newValue}' WHERE `products`.`id` = '{productId}'".format(parameter= parameter, newValue= newValue ,productId=productId)
        cursor.execute(sql)
        db.commit()
        return
    
    @classmethod
    def deleteProduct(self, db, productId:str)-> 0:
        cursor = db.cursor()
        sql = "DELETE FROM products WHERE `products`.`id` = '{productId}'".format(productId=productId)
        cursor.execute(sql)
        db.commit()
        return 
    
    @classmethod
    def deleteProductsWithSellerId(self, db, sellerId:str)->0:
        cursor = db.cursor()
        sql = "DELETE FROM products WHERE `products`.`sellerId` = '{sellerId}'".format(sellerId=sellerId)
        cursor.execute(sql)
        db.commit
        return

    @classmethod
    def deleteAccount(self, db, userType:str, userId:str) -> 0:
        cursor = db.cursor()
        if userType == 'seller':
            Product.deleteProductsWithSellerId(db, userId)
            table = 'seller_users'
        else:
            table = 'client_users'
        sql = "DELETE FROM {table} WHERE `{table}`.`id` = '{userId}'".format(table=table,userId=userId)
        cursor.execute(sql)
        db.commit()
        return 
    
    @classmethod
    def deleteProductFromCart(self, db, productId:str, clientId:str)->0:
        cursor = db.cursor()
        sql = "DELETE FROM cart_products WHERE `cart_products`.`productId` = '{productId}' AND `cart_products`.`clientId` = '{clientId}'".format(productId=productId, clientId=clientId)
        cursor.execute(sql)
        db.commit
        return
    
    @classmethod
    def deleteProductFromCartSeller(self, db, productId):
        cursor = db.cursor()
        sql = "DELETE FROM cart_products WHERE `cart_products`.`productId` = '{productId}'".format(productId=productId)
        cursor.execute(sql)
        db.commit
        return

    @classmethod # Executes when an order is paid
    def deleteProductFromCartClient(self, db, clientId):
        cursor = db.cursor()
        sql = "DELETE FROM cart_products WHERE `cart_products`.`clientId` = '{clientId}'".format(clientId=clientId)
        cursor.execute(sql)
        db.commit
        return

    @classmethod
    def addToCart(self, db, productId, sellerId, clientId, productPrice)->0:
    #id, productId, sellerId, clientId, productPrice, deliveryDate
        orderId = uuid.uuid4()
        cursor = db.cursor()
        sql = "INSERT INTO `cart_products` (`id`, `productId`, `sellerId`, `clientId`, `productPrice`, `deliveryDate`) VALUES ('{orderId}', '{productId}', '{sellerId}', '{clientId}', '{price}', '')".format(orderId=orderId, productId=productId, sellerId=sellerId, clientId=clientId, price=productPrice)
        cursor.execute(sql)
        db.commit()
        return

        

    

