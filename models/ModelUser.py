from .entities.User import Client, Seller

class ModelUser():
    @classmethod
    def login(self, db, user, sql, userType):
        def checkPassword(db_password, userPassword):
            response = False
            if userPassword == db_password:
                response = True
            else:
                response = False 
            return response
        
        try:
            cursor = db.cursor()

            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                if userType == "client":
                                 # id, email, password, fullname, username, postal_code, adress, city, phone
                    user = Client(row[0], row[1], checkPassword(row[2], user.password), row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                    return user
                            
                elif userType == "seller":
                                 # id, email, password, ceoName, companyName
                    user = Seller(row[0], row[1], checkPassword(row[2], user.password), row[3], row[4], row[5])
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
    def get_by_id_client(self, db, id):
        try:
            cursor = db.cursor()
            sql = "SELECT id, email, username, fullname, password, postal_code, adress, city, phone,userType FROM client_users WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                print(row)
                        # id, email, password, fullname, username, postal_code, adress, city, phone, userType
                return Client(row[0], row[1], None, row[3], row[2], row[5], row[6], row[7], row[8], row[9]) 
            elif row == None:
                sql = "SELECT id, email, ceoName, companyName, userType FROM seller_users WHERE id = '{}'".format(id)
                cursor.execute(sql)
                row = cursor.fetchone()
                print(row)
                        # id, email, password, ceoName, companyNmae, userType
                return Seller(row[0], row[1], None, row[2], row[3], row[4])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    


        