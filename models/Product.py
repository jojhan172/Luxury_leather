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
        

    

