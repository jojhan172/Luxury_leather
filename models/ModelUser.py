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
            sql = "SELECT id, email, username, fullname, password FROM client_users WHERE email = '{}'".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], checkPassword(row[4], user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)