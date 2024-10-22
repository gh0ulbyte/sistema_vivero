from conexion import Conexion
from datetime import datetime


def nueva_planta(especie, cajon, cantidad):
    try:
    
        conexion=Conexion()
        cursor=conexion.conectar()
        sql="insert into planta(especie,cajon, cantidad_plantines)"
        sql+=" value('"+especie+"',"+str(cajon)+","+str(cantidad)+");"
        print(sql)
        cursor.execute(sql)
        cursor.execute('commit')
        return True
    except Exception as e:
        print (e)
        return False
    finally:
        conexion.desconectar()
        
        
def buscar_planta_simple(id_planta):
    try:
        conexion=Conexion()
        cursor=conexion.conectar()
        sql="select especie, cantidad_plantines from planta "
        sql+=" where id_planta="+str(id_planta)
        cursor.execute(sql)
        cursor.execute('commit')
        return True, " "
    except Exception as e:
        print (e)
        return False, " "
    finally:
        conexion.desconectar()
        
def buscar_planta(especie):
    try:
        conexion = Conexion()
        cursor = conexion.conectar()
        sql = "SELECT id_planta, especie, cajon FROM planta WHERE especie LIKE '%" + especie + "%'"
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
        conexion=Conexion()
        cursor=conexion.conectar()
        sql="select cantidad_plantines from planta where id_planta="+str(id_planta)
        cursor.execute(sql)
        resultado=cursor.fetchone()
        
        if resultado:
            stock_actual=resultado[0]
            if stock_actual>cantidad:
                nuevo_stock=stock_actual-cantidad
                sql="update planta set cantidad_plantines="+str(nuevo_stock)+" where id_planta="+str(id_planta)
                cursor.execute(sql)
                cursor.execute('commit')
                print(f'Se vendieron {cantidad} de articulos. Nuevo stock:{nuevo_stock}')
                
            else:
                print(f'No hay suficiente Stock :{stock_actual}.')
                
        else:
            print('Articulo no encontrado...')
    except Exception as e:
        print(e)
    finally:
        conexion.desconectar()
        
        
#RIEGO

def riego_auto():
    try:
        conexion=Conexion()
        cursor=conexion.conectar()        
        sql="select riego_auto from riego order by especie limit 1  "   
        cursor.execute(sql)
        plantas=cursor.fetchone()
        return True, plantas
    except Exception as e:
        print(e)
        return False, None
    finally:
        conexion.desconectar()
        
def habilitar_auto():
    try:
        conexion=Conexion()
        cursor=conexion.conectar()
        sql="update riego set riego_auto:'habilitado'"
        cursor.execute(sql)
        cursor.execute('commit')
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conexion.desconectar()
        
def deshabilitar_auto():
    try:
        conexion=Conexion()
        cursor=conexion.conectar()
        sql="update riego set riego_auto:'deshabilitado'"
        cursor.execute(sql)
        cursor.execute('commit')
        return True
    except Exception as e:
        print (e)
        return False
    finally:
        conexion.desconectar()
        
def guardar_fecha(fecha_actual):
        
        try:
            fecha_actual = datetime.now().strftime("%d-%m-%Y")
            conexion=Conexion()
            cursor=conexion.conectar()
            
        
            with cursor:
                sql="INSERT INTO riego (fecha_ultimo) VALUES ('"+ (fecha_actual,)+"') ;"
                print(f"Fecha guardada: {fecha_actual}")
                cursor.execute(sql)
                cursor.execute('commit')
        except Exception as e:
            print(e)
            
        finally:
            conexion.desconectar()
            
            
def nueva_planta_riego(planta, fecha_ultimo):
    try:
        conexion=Conexion()
        cursor=conexion.conectar()
        sql="insert into riego(planta, fecha_ultimo) "
        sql+=" value("+str(planta)+",'"+fecha_ultimo+"');"
        cursor.execute(sql)
        cursor.execute('commit')
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conexion.desconectar()