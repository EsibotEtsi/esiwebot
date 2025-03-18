from werkzeug.security import check_password_hash
from flask_login import UserMixin

"""
Clase Usuario que contendrá los datos de un usuario concreto, así como un método para su autenticación
"""
class User(UserMixin):
    def __init__(self, id, username, nombre, email, fecha, roles, password_hash) -> None:
        self.id = id
        self.username = username
        self.nombre = nombre
        self.email = email
        self.fecha = fecha
        self.roles = roles
        self.password_hash = password_hash
        
        #################################################################
        #   Los permisos de un usuario siguen la estructura:            #
        #       ADMIN - MIEMBRO - REDACTOR - CURSOS                     #
        #   Se almacenan como VARCHAR en la BBDD separados por coma,    #
        #   y se convierten en una lista de permisos al ser cargados    #
        #################################################################
    
    @classmethod
    def check_password(self, password_hash, password):
        
        return check_password_hash(password_hash, password)
