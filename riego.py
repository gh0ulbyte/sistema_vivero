from abc import ABC, abstractmethod
import time
from datetime import datetime
from tkinter import messagebox, Label, Button
from modelo import guardar_fecha


class Riego(ABC):
    
    @abstractmethod
    def automatizacion():
        pass
    

        
        
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
        
        
#----------------------------------------------        
class CuentaRegresiva():
    def __init__(self, master):
        self.master = master
        self.master.title("Regar ahora")

        self.tiempo_restante = 10 
        self.label_tiempo = Label(master, text="", font=("Helvetica", 24))
        self.label_tiempo.pack(pady=20)

        self.boton_iniciar = Button(master, text="Iniciar Riego manualmente", command=self.iniciar_cuenta_regresiva)
        self.boton_iniciar.pack(pady=10)



    def iniciar_cuenta_regresiva(self):
        try:
            fecha_actual = datetime.now().strftime("%d-%m-%Y")
            guardar_fecha(fecha_actual)  
        except Exception as e:
            print(f"Error al guardar la fecha: {e}")

        self.boton_iniciar.pack_forget()
        self.actualizar_tiempo()




    def actualizar_tiempo(self):
        if self.tiempo_restante > 0:
            self.label_tiempo.config(text=f"Llaves de riego abiertas: {self.tiempo_restante}")
            self.tiempo_restante -= 1
            self.master.after(1000, self.actualizar_tiempo) 
        else:
            self.label_tiempo.config(text="¡Llaves Cerradas!")
            messagebox.showinfo('ATENCION', 'Se grabó la fecha de ultimo riego')
            messagebox.showwarning('ATENCION','Se deshabilito el riego automático')          


