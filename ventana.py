import tkinter
from datetime import datetime
import calendar
import time
from tkinter import Toplevel, Label, Menu
from tkinter import messagebox, Frame, Entry, Button, StringVar
from PIL import Image, ImageTk
from tkinter import ttk, END
from modelo import nueva_planta
from modelo import buscar_planta
from modelo import listar_planta, buscar_planta_simple
from modelo import riego_auto
from modelo import vender_planta, guardar_fecha
from modelo import habilito, deshabilito
from modelo import stock_planta
from riego import Llave, CuentaRegresiva
import threading



class Ventana_Grow(Frame):
    def __init__(self, ppal):
        super().__init__()
        
        self.ppal=ppal
        self.configuro_ventana()
        self.bienvenida()
        self.menu_principal()
        self.id_planta=StringVar()
        self.especie=StringVar()
        self.habilitado= StringVar()
        self.cantidad=StringVar()
        self.cantidad_venta=StringVar()
        self.cajon=StringVar()
        self.cantidad_stock=StringVar()
        
        self.sistema_habilitado=True
        
        hilo_riego = threading.Thread(target=riego_auto)
        hilo_riego.daemon = True
        hilo_riego.start()    
        
    def bienvenida(self):
        if self.configuro_ventana:
            messagebox.showinfo('Hola!', 'Bienvenido a Grow System!')
        else:
            pass
        
    def configuro_ventana(self):
        self.ppal.geometry("600x400")
        self.ppal.title("Grow System")
        
        
        image_path = 'fondo.png'
        
        try:
            self.bg_image = Image.open(image_path)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = Label(self.ppal,bg='#89F08C', image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f'Error cargando la imagen: {e}')
            self.ppal.config(bg='#89F08C')
            
#MENU PLANTA (Principal)


    def menu_principal(self):
        self.menu_bar = Menu()
        self.menu_ppal = Menu(self.menu_bar, tearoff=0)
        self.menu_ppal.add_command(label='Nueva Planta', command=self.nueva_planta1)
        self.menu_ppal.add_command(label='Listar Planta', command=self.listar_plantas)
        self.menu_ppal.add_command(label='Buscar Planta', command=self.buscar_planta2)
        self.menu_ppal.add_command(label='Venta ', command=self.venta)
        self.menu_ppal.add_command(label='Agregar Stock', command=self.stock_plantas)
        self.menu_bar.add_cascade(label='Planta', menu=self.menu_ppal)
        
      #Menu RIEGO
        
        self.menu_scn = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Riego', menu=self.menu_scn)
        self.menu_scn.add_command(label='Riego Automatico', command=self.riego_automatico_ventana)
        #self.menu_scn.add_command(label='Nuevo Riego', command=self.nueva_riego_planta)
        
        
        self.ppal.config(menu=self.menu_bar)
    
    
    
    #Listar Plantas
    def listar_plantas(self):
        self.ven_planta = Toplevel(self.ppal)
        self.ven_planta.config(bg='#89F08C')
        self.ven_planta.grab_set()
        self.ven_planta.resizable(0, 0)
        self.ven_planta.geometry('450x450')
        self.ven_planta.title("Listado de Plantas")

        self.grilla = ttk.Treeview(self.ven_planta, columns=('col1', 'col2', 'col3'))
        self.grilla.place(x=5, y=5, width=400, height=400)

        self.grilla.column('#0', width=20, anchor='ne')
        for col in range(1, 4):
            self.grilla.column(f'col{col}', width=80, anchor='nw')

        self.grilla.heading('#0', text='ID Planta')
        for i, text in enumerate(['Especie', 'Cajon','Cantidad Plantines'], start=1):
            self.grilla.heading(f'col{i}', text=text)

        btn_cerrar = Button(self.ven_planta, text='Cerrar', command=self.ven_planta.destroy)
        btn_cerrar.place(x=200, y=360)

        respuesta, plantas = listar_planta()
        if respuesta:
            if plantas:
                for fila in plantas:
                    print(fila)  
                    self.grilla.insert("", END, text=fila[0], values=fila[1:])
            else:
                print("No se encontraron plantas")
        else:
            print("Error al obtener las plantas")

                
        
    def salir(self):
        if messagebox.askyesno("Cerrar", "Confirma cerrar?"):
            self.ppal.destroy()
    
    
    #Agregar plantas (Nueva planta)
            
    def nueva_planta1(self):
        self.ven_plantita=Toplevel(self.ppal)
        self.ven_plantita.geometry('400x400')
        self.ven_plantita.title('Nueva Planta')
        self.label1=Label(self.ven_plantita, text='Especie: ').place(x=2,y=50)
        self.label2=Label(self.ven_plantita, text='Cajon N°:').place(x=2, y=100)
        self.label3=Label(self.ven_plantita, text='Cantidad plantines:').place(x=2, y=150)
        self.text_especie=Entry(self.ven_plantita,textvariable=self.especie, font=16).place(x=110, y=50)
        self.text_cajon=Entry(self.ven_plantita, textvariable=self.cajon, font=16).place(x=110,y=100)
        self.text_cantidad=Entry(self.ven_plantita, textvariable=self.cantidad,font=16).place(x=110, y=150)
        self.btn_grabar=Button(self.ven_plantita, text="Grabar", command=self.grabar_planta).place(x=10, y=200)
        self.btn_cerrar=Button(self.ven_plantita, text="Cerrar", command=self.ven_plantita.destroy).place(x=60, y=200)
        
    def grabar_planta(self):
        try:
            
            if nueva_planta(self.especie.get(), self.cajon.get(), self.cantidad.get()):
                messagebox.showinfo("Grabar Planta", "La planta se ha grabado correctamente")
                self.ven_plantita.destroy()
            
            else:
                messagebox.showerror("Grabar Planta", "No se pudo guardar la planta o ya existe, compruebe stock")
        except Exception as e:
            print(e)
            
    def stock_plantas(self):
        self.ven_stock=Toplevel(self.ppal)
        self.ven_stock.geometry('400x400')
        self.ven_stock.title('Agregar Stock')
        label1=Label(self.ven_stock, text='ID Planta').place(x=2 , y=10)
        text_id=Entry(self.ven_stock, textvariable=self.id_planta, font=16).place(x=60,y=10)
        btn_buscar=Button(self.ven_stock, text='Buscar', command=self.stock_actual).place(x=2,y=50)
        label2=Label(self.ven_stock, text='Especie: ').place(x=5, y=80)
        label3=Label(self.ven_stock, text='Cantidad: ').place(x=5, y=120)
        txt_especie=Entry(self.ven_stock, textvariable=self.especie, font=16).place(x=110,y=80)
        txt_cantidad=Entry(self.ven_stock, textvariable=self.cantidad, font=16).place(x=110, y=120)
       
        label4=Label(self.ven_stock, text='Cantidad a reponer: ').place(x=5, y=200)
        text_cant_stock=Entry(self.ven_stock, textvariable=self.cantidad_stock, font=16).place(x=110  ,y=200  )
       
        btn_grabar=Button(self.ven_stock, text='Guardar', command=self.guardo).place(x=120, y=240)
        
    def stock_actual(self):
        try:
            
            id_planta_val = int(self.id_planta.get())  
            respuesta, planta = buscar_planta_simple(id_planta_val)
            
            if respuesta:
                if planta:
                    self.especie.set(planta[0])  
                    self.cantidad.set(planta[1])  
                else:
                    self.especie.set(" ")
                    self.cantidad.set(" ")
                    messagebox.showerror("Buscar Planta", "Planta no encontrada")
            else:
                self.especie.set(" ")
                self.cantidad.set(" ")
                messagebox.showerror("Buscar Planta", "Error en la búsqueda")
        except Exception as e:
            print(e)
    
    def guardo(self):
        try:
            
            cantidad_stock = int(self.cantidad_stock.get())  
            id_planta = int(self.id_planta.get())  

            
            print(f"Intentando reponer {cantidad_stock} plantines de la planta con ID {id_planta}")

            
            stock_exitoso = stock_planta(cantidad_stock, id_planta)
            
            if stock_exitoso:
                print("Stock registrado correctamente.")
                messagebox.showinfo("GRABAR", "Se grabó correctamente.")
                self.ven_stock.destroy()
            else:
                print("No se pudo grabar el stock.")
                messagebox.showerror("Grabar", "No se ha grabado el stock.")
                
        except ValueError:
            print("Valor no válido para la cantidad de venta.")
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para la cantidad.")
        
    
    
    
    
    #Buscar plantas
        
            
    def buscar_planta2(self):
        self.ven_busco=Toplevel(self.ppal)
        self.ven_busco.geometry('400x300')
        self.ven_busco.title('Buscar ID planta')
        self.label1=Label(self.ven_busco, text="Especie").place(x=2, y=10)
        self.text_especie=Entry(self.ven_busco, textvariable=self.especie, font=16).place(x=50,y=10)
        self.btn_busco=Button(self.ven_busco, text='Buscar ', command=self.buscar_planta_2).place(x=2, y=50)
        self.label2=Label(self.ven_busco, text='ID PLANTA: ').place(x=5, y=80)
        self.txt_id_planta=Entry(self.ven_busco, textvariable=self.id_planta, font=16).place(x=100,y=80)
        
        
        
            
    def buscar_planta_2(self):
        respuesta, planta = buscar_planta(self.especie.get())
        
        if respuesta:
            if planta:
                
                self.id_planta.set(planta[0][1])  
                self.cajon.set(planta[0][0])  
                self.cantidad.set(planta[0][2])
            else:
                self.id_planta.set("")
                self.cajon.set("")
                self.cantidad.set("")
                messagebox.showerror("Buscar Planta", "Planta no encontrada")
        else:
            self.id_planta.set("")
            self.cajon.set("")
            self.cantidad.set("")
            messagebox.showerror("Buscar Planta", "Error en la búsqueda")
    
    #VENTA
    
    def venta(self):
        self.ven_buster=Toplevel(self.ppal)
        self.ven_buster.geometry('400x400')
        label1=Label(self.ven_buster, text='ID Planta').place(x=2 , y=10)
        text_id=Entry(self.ven_buster, textvariable=self.id_planta, font=16).place(x=60,y=10)
        btn_buscar=Button(self.ven_buster, text='Buscar', command=self.venta_cosecha).place(x=2,y=50)
        label2=Label(self.ven_buster, text='Especie: ').place(x=5, y=80)
        label3=Label(self.ven_buster, text='Cantidad: ').place(x=5, y=120)
        txt_especie=Entry(self.ven_buster, textvariable=self.especie, font=16).place(x=110,y=80)
        txt_cantidad=Entry(self.ven_buster, textvariable=self.cantidad, font=16).place(x=110, y=120)
       
        label4=Label(self.ven_buster, text='Cantidad a vender: ').place(x=5, y=200)
        text_cant_ven=Entry(self.ven_buster, textvariable=self.cantidad_venta, font=16).place(x=110  ,y=200  )
       
        btn_grabar=Button(self.ven_buster, text='Vender', command=self.vendo).place(x=120, y=240)
        
    def venta_cosecha(self):
        try:
            
            id_planta_val = int(self.id_planta.get())  
            respuesta, planta = buscar_planta_simple(id_planta_val)
            
            if respuesta:
                if planta:
                    self.especie.set(planta[0])  
                    self.cantidad.set(planta[1])  
                else:
                    self.especie.set(" ")
                    self.cantidad.set(" ")
                    messagebox.showerror("Buscar Planta", "Planta no encontrada")
            else:
                self.especie.set(" ")
                self.cantidad.set(" ")
                messagebox.showerror("Buscar Planta", "Error en la búsqueda")
        except Exception as e:
            print(e)
    
    def vendo(self):
        try:
            
            cantidad_venta = int(self.cantidad_venta.get())  
            id_planta = int(self.id_planta.get())  

            
            print(f"Intentando vender {cantidad_venta} artículos de la planta con ID {id_planta}")

            
            venta_exitosa = vender_planta(cantidad_venta, id_planta)
            
            if venta_exitosa:
                print("Venta registrada correctamente.")
                messagebox.showinfo("GRABAR", "Se grabó correctamente.")
                self.ven_buster.destroy()
            else:
                print("No se pudo grabar la venta.")
                messagebox.showerror("Grabar", "No se ha grabado la venta.")
                
        except ValueError:
            print("Valor no válido para la cantidad de venta.")
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para la cantidad.")
        
    def buscar_planta_simple1(self):
        respuesta, planta = buscar_planta_simple(self.id_planta.get())
        
        if respuesta:
            if planta:
                self.especie.set(planta[0][1])  
                self.cantidad.set(planta[0][2])
                
               
            else:
                self.especie.set(" ")
                self.cantidad.set(" ")
                messagebox.showerror("Buscar Planta", "Planta no encontrada")
            return True, " "    
        else:
            self.especie.set(" ")
            self.cantidad.set(" ")
            messagebox.showerror("Buscar Planta", "Error en la búsqueda")
            return False, " "
    
    
    
    
    
    #Riego
    def riego_automatico_ventana(self):
            self.riego_ven = Toplevel(self.ppal)
            self.riego_ven.geometry('400x400')
            self.riego_ven.title('Riego Automático')
            
            self.label1 = Label(self.riego_ven, text='Riego Automático').place(x=2, y=10)
            self.entrada_estado = Entry(self.riego_ven, width=30)
            self.entrada_estado.place(x=2, y=50)
            
            self.btn_habilitar = Button(self.riego_ven, text='Habilitar Riego', command=self.habilitar_sistema).place(x=10, y=100)
            self.btn_deshabilitar = Button(self.riego_ven, text='Deshabilitar Riego', command=self.deshabilitar_sistema).place(x=10, y=140)
            self.btn_verificar = Button(self.riego_ven, text='Verificar Estado', command=self.verificar_estado).place(x=180, y=50)
            self.btn_regar_ya=Button(self.riego_ven, text='Regar ahora', command=self.riego_manual).place(x=180, y=80)
            
            
    def verificar_estado(self):
        estado = "Activado" if self.sistema_habilitado else "Desactivado"
        self.entrada_estado.delete(0, END)
        self.entrada_estado.insert(0, estado)

    def habilitar_sistema(self):
        self.sistema_habilitado = True
        messagebox.showinfo('Riego Automático', 'Sistema de riego habilitado a las 18:00')
        habilito()

    def deshabilitar_sistema(self):
        self.sistema_habilitado = False
        messagebox.showwarning('Advertencia', 'Sistema de riego deshabilitado')
        deshabilito()
        
        
    def riego_auto(self):
        hora_programada = "18:00"
        while True:
            if self.sistema_habilitado:
                hora_actual = datetime.now().strftime("%H:%M")
                if hora_actual == hora_programada:
                    ventana_cuenta_regresiva=Toplevel(self.ppal)
                    CuentaRegresiva(ventana_cuenta_regresiva)
                    Llave(ventana_cuenta_regresiva)
                    print("Sistema de riego activado")
                    
                    guardar_fecha()
                    time.sleep(60)  
            time.sleep(30)    
  
    
  
    
    def riego_manual(self):
        ventana_cuenta_regresiva = Toplevel(self.ppal)
        CuentaRegresiva(ventana_cuenta_regresiva)
        Llave(ventana_cuenta_regresiva)
        self.sistema_habilitado = False
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        guardar_fecha(fecha_actual)  
        deshabilito()
        
        
            
