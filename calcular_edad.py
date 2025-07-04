import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import date
from dataclasses import dataclass
import calendar

# ---------------------------------------------------------------------------
# 1. LÓGICA DEL PROGRAMA (Back-end) - Sin cambios
# ---------------------------------------------------------------------------

@dataclass
class Edad:
    anios: int
    meses: int
    dias: int
    dias_totales: int

class Persona:
    # ... (Clase Persona sin cambios)
    def __init__(self, nombre: str, fecha_nacimiento: date):
        self.nombre = nombre.strip()
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if fecha_nacimiento > date.today():
            raise ValueError("La fecha de nacimiento no puede ser en el futuro.")
        self.fecha_nacimiento = fecha_nacimiento

    def calcular_edad(self) -> Edad:
        hoy = date.today()
        anios = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            anios -= 1
        meses = hoy.month - self.fecha_nacimiento.month
        dias = hoy.day - self.fecha_nacimiento.day
        if dias < 0:
            meses -= 1
            ultimo_dia_mes_anterior = calendar.monthrange(hoy.year, hoy.month - 1 if hoy.month > 1 else 12)[1]
            dias += ultimo_dia_mes_anterior
        if meses < 0:
            meses += 12
        dias_totales = (hoy - self.fecha_nacimiento).days
        return Edad(anios=anios, meses=meses, dias=dias, dias_totales=dias_totales)

# ---------------------------------------------------------------------------
# 2. INTERFAZ GRÁFICA (Front-end) - Con las mejoras aplicadas
# ---------------------------------------------------------------------------

class CalculadoraEdadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Edad 🧠")
        self.root.resizable(False, False)
        
        # MEJORA 1: Añadir un icono a la ventana.
        # Nota: Debes tener un archivo 'icono.ico' en la misma carpeta
        # o reemplazar 'icono.ico' con la ruta completa a tu archivo.
        try:
            self.root.iconbitmap('icono.ico')
        except tk.TclError:
            print("No se encontró el archivo 'icono.ico'. Se usará el icono por defecto.")

        # MEJORA 2: Aplicar estilos y colores.
        self.root.config(bg='#eaf2f8') # Un fondo azul claro para la ventana

        main_frame = tk.Frame(root, padx=20, pady=20, bg='#eaf2f8')
        main_frame.pack()

        # --- Widgets con estilo ---
        label_nombre = tk.Label(main_frame, text="¿Cómo te llamás?:", font=("Helvetica", 11), bg='#eaf2f8')
        label_nombre.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.entry_nombre = tk.Entry(main_frame, width=40, font=("Helvetica", 11), relief="solid", bd=1)
        self.entry_nombre.grid(row=1, column=0, pady=(0, 15))
        self.entry_nombre.focus()

        label_fecha = tk.Label(main_frame, text="Seleccioná tu fecha de nacimiento:", font=("Helvetica", 11), bg='#eaf2f8')
        label_fecha.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        hoy = date.today()
        self.cal = Calendar(main_frame, selectmode='day',
                              year=hoy.year - 20, month=hoy.month, day=hoy.day,
                              date_pattern='dd/mm/yyyy',
                              background="#3498db", foreground="white",
                              headersbackground="#2980b9", headersforeground="white",
                              selectbackground="#f39c12", selectforeground="white")
        self.cal.grid(row=3, column=0, pady=(0, 20))

        boton_calcular = tk.Button(main_frame, text="Calcular Edad", 
                                   command=self.calcular_y_mostrar,
                                   font=("Helvetica", 12, "bold"),
                                   bg="#2ecc71", fg="white", # Verde brillante
                                   relief="flat", cursor="hand2") # Borde plano y cursor de mano
        boton_calcular.grid(row=4, column=0, sticky="ew", ipady=5) # ipady hace el botón más alto

        # MEJORA 3: Añadir una etiqueta para mostrar el resultado en la ventana.
        self.label_resultado = tk.Label(main_frame, text="", font=("Helvetica", 11, "italic"),
                                        bg='#eaf2f8', justify="left")
        self.label_resultado.grid(row=5, column=0, pady=(15, 0), sticky="w")


    def calcular_y_mostrar(self):
        nombre = self.entry_nombre.get()
        fecha_nacimiento_str = self.cal.get_date()
        
        if not nombre.strip():
            messagebox.showerror("Error de Validación", "Por favor, ingresá un nombre.")
            return
        
        try:
            dia, mes, anio = map(int, fecha_nacimiento_str.split('/'))
            fecha_nacimiento_obj = date(anio, mes, dia)
        except (ValueError, TypeError):
            messagebox.showerror("Error de Fecha", "La fecha seleccionada no es válida.")
            return
            
        if fecha_nacimiento_obj > date.today():
            messagebox.showerror("Error de Validación", "¡No podés haber nacido en el futuro!")
            return

        try:
            persona = Persona(nombre, fecha_nacimiento_obj)
            edad = persona.calcular_edad()

            resultado_texto = (
                f"¡Hola, {persona.nombre}!\n\n"
                f"Tenés {edad.anios} años, {edad.meses} meses y {edad.dias} días.\n"
                f"(En total, has vivido {edad.dias_totales:,} días)."
            )
            
            # MEJORA 3 (Parte B): Mostrar el resultado en la etiqueta, no en un messagebox.
            self.label_resultado.config(text=resultado_texto)

            # MEJORA 4: Limpiar el campo de nombre para el siguiente cálculo.
            self.entry_nombre.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

# ---------------------------------------------------------------------------
# 3. PUNTO DE ENTRADA DEL PROGRAMA - Sin cambios
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraEdadApp(root)
    root.mainloop()