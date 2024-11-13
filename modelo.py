from conexion import Conexion
from datetime import datetime


def nueva_planta(especie, cajon, cantidad):
    try:
        conexion = Conexion()
        cursor = conexion.conectar()

        
        sql = "INSERT INTO planta (especie, cajon, cantidad_plantines) VALUES (%s, %s, %s);"
        cursor.execute(sql, (especie, cajon, cantidad))  

        
        planta = cursor.lastrowid

       
        sql_riego = "INSERT INTO riego (planta, fecha_ultimo) VALUES (%s, NULL);"
        cursor.execute(sql_riego, (planta,))  

        
        cursor.execute('commit')
        print("Planta y registro de riego guardados correctamente.")
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conexion.desconectar()

        
        
def buscar_planta_simple(id_planta):
    try:
        conexion = Conexion()
        cursor = conexion.conectar()
        sql = f"select especie, cantidad_plantines from planta where id_planta={id_planta};"
        print(f"Consultando con SQL: {sql}")  
        cursor.execute(sql)
        planta = cursor.fetchone()  
        
        if planta:
            print(f"Planta encontrada: {planta}")  
            return True, planta
        else:
            print("Planta no encontrada")  
            return False, None
            
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return False, None
    finally:
        conexion.desconectar()
        
def buscar_planta(especie):
    try:
        conexion = Conexion()
        cursor = conexion.conectar()
        sql = "SELECT id_planta, cajon, cantidad_plantines FROM planta WHERE especie LIKE '%" + especie + "%'"
        cursor.execute(sql)
        plantas = cursor.fetchall()
        return True, plantas
    except Exception as e:
        print(e)
        return False, []
    finally:
        conexion.desconectar()

        
def listar_planta():
    try:
        conexion = Conexion()
        cursor = conexion.conectar()
        sql = """
        SELECT id_planta, especie, cajon, cantidad_plantines
        FROM planta
        WHERE cantidad_plantines>=1 
        ORDER BY especie
        """
        cursor.execute(sql)
        plantas = cursor.fetchall()
        return True, plantas
    except Exception as e:
        print(e)
        return False, None
    finally:
        conexion.desconectar()
        
def vender_planta(cantidad, id_planta):
    try:
        conexion = Conexion()
        cursor = conexion.conectar()
        
        
        sql = f"select cantidad_plantines from planta where id_planta={id_planta}"
        print(f"Consulta SQL: {sql}")
        cursor.execute(sql)
        resultado = cursor.fetchone()
        
        if resultado:
            stock_actual = resultado[0]
            if stock_actual >= cantidad:  
                nuevo_stock = stock_actual - cantidad
                
                sql = f"update planta set cantidad_plantines={nuevo_stock} where id_planta={id_planta}"
                print(f"Actualizando stock: {sql}")
                cursor.execute(sql)
                cursor.execute('commit')
                print(f"Se vendieron {cantidad} artículos. Nuevo stock: {nuevo_stock}")
                return True  
            else:
                print(f"No hay suficiente Stock: {stock_actual}.")
                return False  
        else:
            print("Articulo no encontrado...")
            return False  
        
    except Exception as e:
        print(e)
        return False  
    
    finally:
        conexion.desconectar()
        
        
def stock_planta(cantidad, id_planta):
    try:
        conexion = Conexion()
        cursor = conexion.conectar()
        
        
        sql = f"select cantidad_plantines from planta where id_planta={id_planta}"
        print(f"Consulta SQL: {sql}")
        cursor.execute(sql)
        resultado = cursor.fetchone()
        
        if resultado:
            stock_actual = resultado[0]
            if stock_actual <= 10:  
                nuevo_stock = stock_actual + cantidad
                
                sql = f"update planta set cantidad_plantines={nuevo_stock} where id_planta={id_planta}"
                print(f"Actualizando stock: {sql}")
                cursor.execute(sql)
                cursor.execute('commit')
                print(f"Se agregaron {cantidad} plantines. Nuevo stock: {nuevo_stock}")
                return True  
            else:
                print(f"Hay suficiente Stock: {stock_actual}.")
                return False  
        else:
            print("Articulo no encontrado...")
            return False  
        
    except Exception as e:
        print(e)
        return False  
    
    finally:
        conexion.desconectar()


        
        
#RIEGO

def riego_auto():
    try:
        conexion=Conexion()
        cursor=conexion.conectar()        
        sql="SELECT riego_auto FROM riego LIMIT 1"    
        cursor.execute(sql)
        plantas=cursor.fetchone()
        return True, plantas
    except Exception as e:
        print(e)
        return False, None
    finally:
        conexion.desconectar()
        

        
def guardar_fecha(fecha_actual):
    try:
        conexion = Conexion()
        cursor = conexion.conectar()
       
        
        sql = "UPDATE  riego SET fecha_ultimo= %s WHERE planta IS NOT NULL;"
        cursor.execute(sql, (fecha_actual,))  
        print(f"Fecha guardada:{fecha_actual}")
        cursor.execute('commit')
        print(f"Fecha guardada: {fecha_actual}")
    except Exception as e:
        print(e)
    finally:
        conexion.desconectar()
        
def deshabilito():
    try:
        conexion=Conexion()
        cursor=conexion.conectar()
        
        sql="update riego set riego_auto= 'deshabilitado';"
        
        cursor.execute(sql)
        cursor.execute('commit')
    except Exception as e:
        print(e)
    finally:
        conexion.desconectar()
        
        
def habilito():
    try:
        conexion=Conexion()
        cursor=conexion.conectar()
        
        sql="update riego set riego_auto= 'habilitado';"
        
        cursor.execute(sql)
        cursor.execute('commit')
        
    except Exception as e:
        print(e)
    finally:
        conexion.desconectar()
        
        
            
            
