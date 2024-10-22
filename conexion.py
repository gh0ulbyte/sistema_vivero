import mysql.connector
class Conexion():
    def __init__(self):
        self.conexion=None
        self.cursor=None
        
    def conectar(self):
        self.conexion=mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            passwd='Jesus.033531',
            db='grow_system'
        )
        
        self.cursor=self.conexion.cursor()
        return self.cursor
    
    def desconectar(self):
        self.conexion=None
        self.cursor=None
        
        

         
    
