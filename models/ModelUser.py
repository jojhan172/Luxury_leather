from .entities.User import User

class ModelUser():
    @classmethod
    def login(self, db, user):

        def checkPassword(db, userPassword):
            response = False
            if userPassword == db:
                response = True
            else:
                response = False 
            return response
        
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, password, fullname, username, postal_code, adress, city, phone FROM client_users WHERE email = '{}'".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], checkPassword(row[2], user.password), row[3], row[4], row[5], row[6], row[7], row[8])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, db, id):

        def checkPassword(db, userPassword):
            response = False
            if userPassword == db:
                response = True
            else:
                response = False 
            return response
        
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, password, fullname, username, postal_code, adress, city, phone FROM client_users WHERE id = '{}'".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                
                return User(row[0], row[1], None, row[3], row[4], row[5], row[6], row[7], row[8])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

        