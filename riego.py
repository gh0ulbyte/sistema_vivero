from abc import ABC, abstractmethod
import os
import time

class Riego(ABC):
    
    @abstractmethod
    def automatizacion():
        pass
    
class Cajones_Regados(Riego):
    def __init__(self, cajon_regado):
        self.cajon_regado=cajon_regado
    def automatizacion(self):
        self.cajon_regado=0
                
        for i in range(1,10):
            self.cajon_regado+=1
        
        print(f'cantidad de cajones regados {self.cajon_regado}')
        
        
class Llave(Riego):
    def __init__(self, numero_cajon):
       
        self.numero_cajon=numero_cajon
        
    def automatizacion(self):
        self.apertura_llave()
        time.sleep(10)
        self.cierre_llave()
    
    def apertura_llave(self):
        print('llaves de riego abierta')
    
    
    def cierre_llave(self):
        print('llaves de riego cerrada')