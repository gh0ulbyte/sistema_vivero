import tkinter
from datetime import datetime
import calendar
from tkinter import Toplevel, Label, Menu
from tkinter import messagebox, Frame, Entry, Button, StringVar
from PIL import Image, ImageTk
from tkinter import ttk, END
from modelo import nueva_planta, nueva_planta_riego
from modelo import buscar_planta
from modelo import listar_planta, buscar_planta_simple
from modelo import riego_auto, habilitar_auto, deshabilitar_auto
from modelo import vender_planta, guardar_fecha
from riego import Riego,Llave



class Ventana_G(Frame):
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
        self.fecha_riego=StringVar()
        
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
        self.ven_planta.geometry('600x600')
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
        label1=Label(self.ven_plantita, text='Especie: ').place(x=2,y=50)
        label2=Label(self.ven_plantita, text='cajon:').place(x=2, y=100)
        label3=Label(self.ven_plantita, text='cantidad plantines:').place(x=2, y=150)
        text_especie=Entry(self.ven_plantita,textvariable=self.especie, font=16).place(x=100, y=50)
        text_cajon=Entry(self.ven_plantita, textvariable=self.cajon, font=16).place(x=100,y=100)
        text_cantidad=Entry(self.ven_plantita, textvariable=self.cantidad,font=16).place(x=100, y=150)
        btn_grabar=Button(self.ven_plantita, text="Grabar", command=self.grabar_planta).place(x=10, y=200)
        btn_cerrar=Button(self.ven_plantita, text="Cerrar", command=self.ven_plantita.destroy).place(x=60, y=200)
        
    def grabar_planta(self):
        try:
            
            if nueva_planta(self.especie.get(), self.cajon.get(), self.cantidad.get()):
                messagebox.showinfo("Grabar Planta", "La planta se ha grabado correctamente")
                self.ven_plantita.destroy()
            
            else:
                messagebox.showerror("Grabar Planta", "No se pudo guardar la planta o ya existe, compruebe stock")
        except ValueError:
            messagebox.showerror('Error', 'Ingrese una fecha valida con el formato DD-MM-YYYY')
    
    
    #Buscar plantas
        
            
    def buscar_planta2(self):
        self.ven_busco=Toplevel(self.ppal)
        self.ven_busco.geometry('400x300')
        label1=Label(self.ven_busco, text="Especie").place(x=2, y=10)
        text_especie=Entry(self.ven_busco, textvariable=self.especie, font=16).place(x=50,y=10)
        btn_busco=Button(self.ven_busco, text='Buscar ', command=self.buscar_planta_2).place(x=2, y=50)
        label2=Label(self.ven_busco, text='ID PLANTA: ').place(x=5, y=80)
        txt_id_planta=Entry(self.ven_busco, textvariable=self.id_planta, font=16).place(x=100,y=80)
        
        
        
            
    def buscar_planta_2(self):
        respuesta, planta = buscar_planta(self.especie.get())
        
        if respuesta:
            if planta:
                self.id_planta.set(planta[0][0])  
                self.cajon.set(planta[0][1])
                self.cantidad.set(planta[0][2])
            else:
                self.id_planta.set(" ")
                self.cajon.set(" ")
                self.cantidad.set(" ")
                messagebox.showerror("Buscar Planta", "Planta no encontrada")
        else:
            self.id_planta.set(" ")
            self.cajon.set(" ")
            self.cantidad.set(" ")
            messagebox.showerror("Buscar Planta", "Error en la búsqueda")
    
    
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
        
        respuesta, planta = buscar_planta_simple(self.id_planta.get()) 
        
        if respuesta:
            if planta:
                self.especie.set(planta[0][1])  
                self.cantidad.set(planta[0][2])
               
            else:
                self.especie.set(" ")
                self.cantidad.set(" ")
                messagebox.showerror("Buscar Planta", "Planta no encontrada")
        else:
            self.id_planta.set(" ")
            self.cantidad.set(" ")
            messagebox.showerror("Buscar Planta", "Error en la búsqueda")
            
    
    def vendo(self):
        if vender_planta(self.id_planta.get(), self.cantidad.get()):
            messagebox.showinfo("GRABAR", "Se grabo correctamente.")
            self.ven_buster.destroy()
        else:
            messagebox.showerror("Grabar", "No se ha grabado la venta.")
    
        
        
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
        
        
    def nueva_riego_planta(self):
        self.ven_plantita_riego=Toplevel(self.ppal)
        self.ven_plantita_riego.geometry('400x400')
        label1=Label(self.ven_plantita_riego, text='ID Planta: ').place(x=2,y=50)
        label2=Label(self.ven_plantita_riego, text='Fecha de Riego:').place(x=2, y=100)
        text_planta=Entry(self.ven_plantita_riego,textvariable=self.id_planta, font=16).place(x=100, y=50)
        text_fecha=Entry(self.ven_plantita_riego, textvariable=self.fecha_riego, font=16).place(x=100,y=100)
        btn_grabar=Button(self.ven_plantita_riego, text="Grabar", command=self.grabar_planta_riego).place(x=10, y=200)
        btn_cerrar=Button(self.ven_plantita_riego, text="Cerrar", command=self.ven_plantita_riego.destroy).place(x=60, y=200)
        
    def grabar_planta_riego(self):
        try:
            fecha_ingresada=datetime.strptime(self.fecha_riego.get(), '%d-%m-%Y')
        
            if nueva_planta_riego(self.id_planta.get(), fecha_ingresada):
                if self.fecha_riego.get() in calendar:
                    messagebox.showinfo("Grabar Riego", "La nueva fecha de riego se ha grabado correctamente")
                    self.ven_plantita_riego.destroy()
                    self.riego='si'
            
            else:
                messagebox.showerror("Grabar Riego", "No se pudo guardar la fecha")  
        except ValueError:
            messagebox.showerror('Error', 'Ingrese una fecha valida en formato DD-MM-YYYY')    
            
    def ultimo_riego_planta(self):
        
        self.ven_busco=Toplevel(self.ppal)
        self.ven_busco.geometry('400x300')
        label1=Label(self.ven_busco, text="ID Planta").place(x=2, y=10)
        text_planta=Entry(self.ven_busco, textvariable=self.id_planta, font=16).place(x=60,y=10)
        #btn_busco=Button(self.ven_busco, text='Buscar ', command=self.buscar_planta_regada).place(x=2, y=50)
        label2=Label(self.ven_busco, text='Fecha ultimo RIEGO: ').place(x=5, y=80)
        label3=Label(self.ven_busco, text='ID RIEGO: ').place(x=5, y=120)
        #txt_fecha=Entry(self.ven_busco, textvariable=self.fecha_ultimo, font=16).place(x=120,y=80)
        #txt_id_riego=Entry(self.ven_busco, textvariable=self.id_riego, font=16).place(x=110, y=120)
          
   # def buscar_planta_regada(self):
    #    respuesta, plantas = buscar_riego(self.id_planta.get())
        
    #    if respuesta:
    #        if plantas:
    #            self.fecha_ultimo.set(plantas[0][1])  
    #            self.id_riego.set(plantas[0][2])
    #        else:
    #            self.fecha_ultimo.set(" ")
    #            self.id_riego.set(" ")
    #            messagebox.showerror("Buscar RIEGO", "RIEGO no encontrada")
    #    else:
    #        self.fecha_ultimo.set(" ")
    #        self.id_riego.set(" ")
    #        messagebox.showerror("Buscar RIEGO", "Error en la búsqueda")

    def riego_automatico_ventana(self):
        self.riego_ven=Toplevel(self.ppal) 
        self.riego_ven.geometry('400x400')
        label1=Label(self.riego_ven, text='Riego automatico').place(x=2, y=10)
        btn_buscar=Button(self.riego_ven, text='Buscar', command=self.busco_auto).place(x=150, y=50)
        txt_habilitado=Entry(self.riego_ven, textvariable=self.habilitado).place(x=2, y= 50)
        btn_habilitar=Button(self.riego_ven, text='Habilitar Riego', command=self.habilito_riego).place(x=10, y=100)
        btn_deshabilitar=Button(self.riego_ven, text='Deshabilitar Riego', command=self.deshabilito_riego).place(x=10, y=140)
        btn_regar=Button(self.riego_ven, text='Regar ahora', command=self.riego_ya_boton)
        btn_regar.pack(pady=10)
    
    def riego_ya_boton(self):
        ventana_cuenta_regresiva=Toplevel(self.ppal)
        CuentaRegresiva(ventana_cuenta_regresiva)
        Llave(ventana_cuenta_regresiva)
        
        
        
   
        
    def habilito_riego(self):
        try: 
            respuesta, auto=habilitar_auto()
            if respuesta:
                return True, auto
            else:
                return False, " "
        except Exception as e:
            print(e)
        finally:
            pass
            
        
    
    def deshabilito_riego(self):
        
        respuesta, auto=deshabilitar_auto()
        if respuesta:
            return True, auto
        else:
            return False, " "    
        
     
    def busco_auto(self):
        respuesta, auto=riego_auto()
        if respuesta:
            return True, auto
        else:
            return False, " "
            

    #Riego manual y comprobacion de riego.
    
    
    
   
    
    
    
            
class CuentaRegresiva:
    def __init__(self, master):
        self.master = master
        self.master.title("Regar ahora")

        self.tiempo_restante = 10 
        self.label_tiempo = Label(master, text="", font=("Helvetica", 24))
        self.label_tiempo.pack(pady=20)

        self.boton_iniciar = Button(master, text="Iniciar Riego manualmente", command=self.iniciar_cuenta_regresiva)
        self.boton_iniciar.pack(pady=10)



    def iniciar_cuenta_regresiva(self):
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        guardar_fecha(fecha_actual)
    
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
