import uuid # libreria para crear ids unicos  --> uuid.uuid4()

"""
    Estos diccionarios contendran todos los datos del usuario, su llave sera el IdNumber
    de cada usuario, y sus valores serán listas con los datos de cada usuarios
"""

clientUsers = {}
sellerUsers = {} 
products = {}
"""
Dentro de la web, se tendran dos opcioes por lo que la variable userType podrá ser 
client o seller
el usuario tipo admin será un usuario ya existente que se debera registrar de otro modo
"""

clientType = "client"
sellerType = "seller"

def createUser():
    cliente = Client("Osiris", "123", "jojhan@email.com", 121212, "Dg. 40 #37.183", "Bogota", 3221239876 )
    vendedor = Seller("Osiris", "123", "jojhan@email.com", 5)
    cliente.addUser()
    vendedor.addUser()
    #producto = Product(vendedor.idNumber)
    print(f"Se creo un nuevo cliente -> {clientUsers} \n")
    print(f"Se creo un nuevo vendedor -> {sellerUsers} \n ")
    return cliente, vendedor

# Esta funcion crea un producto dentro de la tienda
def addProductToStore(productName, price, quantity):

    sellerId = newSeller.idNumber # Este id lo traemos del diccionario -> pero deberia venir de la pagina -> a su vez esto deberia venir de una base de datos
    Product(sellerId, productName, price, quantity).addProduct()
    print(f"Tarea completada se aniadio un nuevo producto a la tienda, el producto fue: {productName} con una cantidad de: {quantity}. Fue aniadido por el vendedor {sellerId}")
    
    #producto1 = Product(main[1].idNumber, "Jorda 1", 200000, 5)

def createOrder():
    productsList = []
    clientId = newClient.idNumber
    deliveryCity = newClient.city
    deliveryAdress = newClient.deliveryAdress
    postalCode = newClient.postalCode

    for i in range(len(productsKeys)):
        productsList.append(productsKeys[i])
        
    newOrder = Order(clientId, productsList, deliveryCity, deliveryAdress, postalCode)
    print(f"La orden se creo correctamente, los productos fueron: {productsList}. \nEl cliente que lo creo fue: {clientId}. El destino es: {deliveryAdress} en la ciudad de {deliveryCity}")



# Clase padre, funcionara para crear los usuarios tipo client y seller
class RegisterUser():
    def __init__(self, userName, password, email):
        self.__userName = userName
        self.__password = password
        self.__email = email

# userName Getter and Setter
    @property
    def userName(self):
        ""
        return self.__userName
    
    @userName.setter
    def userName(self, newName):
        self.__userName = newName

    @userName.deleter
    def userName(self):
        del(self.__userName)

# password Getter and Setter
    @property
    def password(self):
        ""
        return self.__password
    
    @password.setter
    def password(self, newPassword):
        self.__password = newPassword

    @password.deleter
    def password(self):
        del(self.__password)

#email Getter and Setter
    @property
    def email(self):
        ""
        return self.__email
    
    @email.setter
    def email(self, newPassword):
        self.__email = newPassword

    @email.deleter
    def email(self):
        del(self.__email)


class Client(RegisterUser):
    def __init__(self, userName, password, email, postalCode, adress, city, phone):
        """
        Inicializa los atributos de la clase padre,
        luego inicializa los atributos de la clase hijo
        con la función super()
        """
        super().__init__(userName, password, email)
        idNumber = uuid.uuid4()
        self.__idNumber = idNumber
        self.__postalCode = postalCode
        self.__adress = adress
        self.__city = city
        self.__phone = phone

    @property
    def idNumber(self):
        ""
        return self.__idNumber
    @idNumber.setter
    def idNumber(self, newIdNumber):
        self.__idNumber = newIdNumber
    @idNumber.deleter
    def idNumber(self):
        del(self.__idNumber)


    @property
    def postalCode(self):
        ""
        return self.__postalCode
    @postalCode.setter
    def postalCode(self, newPostalCode):
        self.__postalCode = newPostalCode
    @postalCode.deleter
    def postalCode(self):
        del(self.__postalCode)

    @property
    def deliveryAdress(self):
        ""
        return self.__adress
    @deliveryAdress.setter
    def deliveryAdress(self, newAdress):
        self.__adress = newAdress

    @deliveryAdress.deleter
    def deliveryAdress(self):
        del(self.__adress)
    
    @property
    def city(self):
        ""
        return self.__city
    @city.setter
    def city(self, newCity):
        self.__city = newCity

    @city.deleter
    def city(self):
        del(self.__city)

    @property
    def phone(self):
        ""
        return self.__phone
    @phone.setter
    def phone(self, newPhone):
        self.__phone = newPhone

    @phone.deleter
    def adress(self):
        del(self.__phone)
        
    # Función para añadir usuario a la base de datos
    def addUser(self):
        userData = [self.__idNumber, clientType, self.userName, self.password, self.email, self.__postalCode, self.__adress, self.__city, self.__phone]
        clientUsers[self.__idNumber] = userData
        return clientUsers


class Seller(RegisterUser):
    def __init__(self, userName, password, email, rating) -> None:
        super().__init__(userName, password, email)
        idNumber = uuid.uuid4()
        self.__idNumber = idNumber
        self.__rating = rating

    @property
    def idNumber(self):
        "si"
        return (self.__idNumber)
    @idNumber.setter
    def idNumber(self, newIdNumber):
        self.__idNumber = newIdNumber
    @idNumber.deleter
    def idNumber(self):
        del(self.__idNumber)

    @property
    def rating(self):
        ""
        return self.__rating
    @rating.setter
    def rating(self, newRating):
        self.__rating= newRating

    @rating.deleter
    def rating(self):
        del(self.__rating)

    def addUser(self):
        userData = [self.__idNumber, sellerType, self.userName, self.password, self.email, self.__rating]
        sellerUsers[self.__idNumber] = userData
        return sellerUsers

class Product():
    def __init__(self, sellerId, productName, price, quantity) -> None:
        """
        Estos ids en esta fase del proyecto se generán con una libreria constantemente,
        la idea con lo vinculacion a una base de datos, es que estos no se generen constantemente
        sino que se generen una unica vez, y asi buscarlos desde la web y la base de datos.
        """
        self.__productId = uuid.uuid4()
        self.__sellerId = sellerId
        self.__productName = productName
        self.__price = price
        self.__quantity = quantity

    @property # --> el ID no deberia cambiar jamas, pues se pierde el rastreo del producto. Por eso no se tiene un setter
    def productId(self):
        ""
        return self.__productId
    @productId.deleter
    def productId(self):
        del(self.__productId)



    @property
    def productName(self):
        ""
        return self.__productName
    @productName.setter
    def rating(self, newRating):
        self.__productName= newRating

    @productName.deleter
    def rating(self):
        del(self.__rating)

    @property
    def price(self):
        ""
        return self.__price
    @price.setter
    def price(self, newPrice):
        self.__price = newPrice

    @price.deleter
    def price(self):
        del(self.__price)

    @property
    def quantity(self):
        ""
        return self.__quantity
    
    @quantity.setter
    def quantity(self, newQuantity):
        self.__quantity = newQuantity

    @quantity.deleter
    def quantity(self):
        del(self.__quantity)
    

    def addProduct(self):
        productData = [self.__productId, self.__sellerId, self.__productName, self.__price, self.__quantity]
        products[self.__productId] = productData
        return products


class Order:

    def __init__(self, clientId, productsList, deliveryCity, deliveryAdress, postalCode,) -> None:
        self.__orderId = uuid.uuid4()
        self.__clientId = clientId
        self.__productsList = productsList
        self.__deliveryCity = deliveryCity
        self.__deliveryAdress = deliveryAdress
        self.__postalCode = postalCode  

    def totalPrice():

        ...

newUsers = createUser()
newClient = newUsers[0]
newSeller = newUsers[1]
clientKeys = clientUsers.keys()
clientKeys = list(clientKeys)
"""id[0], type[1], user name[2], password[3], email[4], postalcode[5], adress[6], city[7], phone[8]"""

sellerKeys = sellerUsers.keys()
sellerKeys = list(sellerKeys)

addProductToStore("Air Jordan 1", 240000, 5)
addProductToStore("Nike SB Dunk 1", 150000, 3)
addProductToStore("Billetera Zerpi", 20000, 10)

productsKeys = products.keys()
productsKeys = list(productsKeys)

print(f"\nLos clientes son: {clientKeys} \nLos vendedores son: {sellerKeys} \nLos productos en la tienda son: {productsKeys}\n")

createOrder()
