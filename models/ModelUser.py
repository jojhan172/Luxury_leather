from .entities.User import Client, Seller

class ModelUser():
    @classmethod
    def client_login(self, db, user):
        def checkPassword(db_password, userPassword):
            response = False
            if userPassword == db_password:
                response = True
            else:
                response = False 
            return response
        
        try:
            cursor = db.cursor()
            sql = "SELECT id, email, password, fullname, username, postal_code, adress, city, phone FROM client_users WHERE email = '{}'".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = Client(row[0], row[1], checkPassword(row[2], user.password), row[3], row[4], row[5], row[6], row[7], row[8])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod  
    def VerifyRegister(self, db, sql):
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return True # Si el usuario existe es True
            else: 
                return False # False si el usuario no existe
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def addToDataBase(self, db, sql):
        try: 
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
 
        except Exception as ex:
            raise Exception(ex)

    @classmethod # metodo para poder mantener el usuario instanciado con flask, esto permite usar lo en las otras paginas de la web
    def get_by_id(self, db, id):
        try:
            cursor = db.cursor()
            sql = "SELECT id, email, password, fullname, username, postal_code, adress, city, phone FROM client_users WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Client(row[0], row[1], None, row[3], row[4], row[5], row[6], row[7], row[8])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

        