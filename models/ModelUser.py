from .entities.User import User
from random import randint
from datetime import datetime
from werkzeug.security import generate_password_hash


class SQLException(Exception):
    def __init__(self, msg):
        self.msg = msg


class ModelUser():

    @classmethod
    def login(self, db, username, password):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT username,  password_hash, nombre, email, fecha, roles, id FROM user WHERE username = '{username}'"
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                if User.check_password(row[1], password):
                    return User(row[6], row[0], row[2], row[3], row[4], row[5].split(","), row[1]) #row[5].split(",") convierte la lista de roles en una lista
                else:
                    return False
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(self, db, username, nombre, email, password):
        try:
            #¿Que se hace aqui con el id exacaamente?
            # cursor = db.connection.cursor()
            # id = randint(10, 10000)
            # sql = f"SELECT 1 FROM user WHERE id = '{id}'"
            # cursor.execute(sql)
            # row = cursor.fetchone()
            # while(row == 1):
            #     id = randint(10, 10000)
            #     sql = f"SELECT 1 FROM user WHERE id = '{id}'"
            #     cursor.execute(sql)
            #     row = cursor.fetchone()
            cursor = db.connection.cursor()
            fecha = datetime.now()
            password_hash = generate_password_hash(password)
            sql = f"""
            insert into user (username, nombre, email, fecha, roles, password_hash) 
                values('{username}', '{nombre}', '{email}', date('{fecha}'), '{'MIEMBRO'}', '{password_hash}');
            """
            print(sql)
            cursor.execute(sql)
            db.connection.commit()

            user = self.login(db, username, password)
            if user == False or user == None:
                raise SQLException("El usuario no ha podido ser registrado")
            else:
                return user

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = f"SELECT username, nombre, email, fecha, roles, id , password_hash FROM user WHERE id = '{id}'"
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                return User(row[5], row[0], row[1], row[2], row[3], row[4], row[6])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
