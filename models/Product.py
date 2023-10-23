class Product():
    """def __init__(self, db, id, price, name, imgURL, sellerId ) -> None:
        self.db = db
        self.id = id
        self.price = price
        self.name = name
        self.imgURL = imgURL
        self.sellerId = sellerId """
    
    @classmethod
    def addToDb(self, db, id, name, price, sellerId, imgURL): # Añade un nuevo producto con los datos que el vendedor proporcione a traves del formulario
        try:
            cursor = db.cursor()
            sql = "INSERT INTO `products` (`id`, `name`, `price`, `sellerId`, `imgURL`) VALUES ('{id}', '{name}', '{price}', '{sellerId}', '{imgURL}')".format(id= id, name=name, price=price, sellerId = sellerId, imgURL = imgURL)
            cursor.excute(sql)
            return True
        except Exception as ex:
            raise Exception(ex)

