import tkinter as tk
from tkinter import messagebox
import math
import json
import os
import matplotlib.pyplot as plt

# CLASE: Calculadora
# PROPÓSITO: Realiza cálculos estadísticos
class Calculadora:
    def __init__(self, datos):
        self.datos = datos

    def media(self):
        # PROPÓSITO: Calcula el promedio
        return sum(self.datos) / len(self.datos)

    def mediana(self):
        # PROPÓSITO: Calcula el valor del centro
        ordenados = sorted(self.datos)
        n = len(ordenados)
        if n % 2 == 0:
            return (ordenados[n//2 - 1] + ordenados[n//2]) / 2
        return ordenados[n//2]

    def moda(self):
        # PROPÓSITO: Valor que más se repite
        freq = {}
        for x in self.datos:
            freq[x] = freq.get(x, 0) + 1
        return max(freq, key=freq.get)

    def desviacion(self):
        # PROPÓSITO: Qué tan dispersos están los datos
        m = self.media()
        return math.sqrt(sum((x - m)**2 for x in self.datos) / len(self.datos))

# CLASE: ManejadorArchivos
# PROPÓSITO: Guarda y carga datos en un archivo JSON
class ManejadorArchivos:
    def __init__(self, archivo):
        self.archivo = archivo

    def guardar(self, datos, resultados):
        # PROPÓSITO: Guarda datos y resultados
        with open(self.archivo, "w") as f:
            json.dump({"datos": datos, "resultados": resultados}, f, indent=4)

    def cargar(self):
        # PROPÓSITO: Carga datos guardados
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                return json.load(f)
        return None

# CLASE: App
# PROPÓSITO: Maneja la interfaz gráfica
class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Calculadora Estadística")
        self.ventana.geometry("400x500")
        self.manejador = ManejadorArchivos("datos.json")
        self.ultimos_datos = []
        self.ultimos_resultados = {}

        tk.Label(ventana, text="Calculadora Estadística",
                 font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(ventana, text="Ingresa números separados por comas:").pack()
        self.entrada = tk.Entry(ventana, width=35, font=("Arial", 11))
        self.entrada.pack(pady=5)

        tk.Button(ventana, text="Calcular", command=self.calcular,
                  width=20).pack(pady=3)
        tk.Button(ventana, text="Ver gráfica", command=self.graficar,
                  width=20).pack(pady=3)
        tk.Button(ventana, text="Guardar", command=self.guardar,
                  width=20).pack(pady=3)
        tk.Button(ventana, text="Cargar", command=self.cargar,
                  width=20).pack(pady=3)
        tk.Button(ventana, text="Limpiar", command=self.limpiar,
                  width=20).pack(pady=3)

        self.resultado = tk.Text(ventana, height=10, width=45,
                                 font=("Arial", 10), state="disabled")
        self.resultado.pack(pady=10)

    def calcular(self):
        # PROPÓSITO: Lee los datos y muestra los resultados estadísticos
        try:
            datos = [float(x.strip()) for x in self.entrada.get().split(",")]
            if len(datos) < 2:
                messagebox.showwarning("Aviso", "Ingresa al menos 2 números.")
                return
            # OBJETO: calc de la clase Calculadora
            calc = Calculadora(datos)
            self.ultimos_datos = datos
            self.ultimos_resultados = {
                "Media": round(calc.media(), 4),
                "Mediana": round(calc.mediana(), 4),
                "Moda": round(calc.moda(), 4),
                "Desviacion": round(calc.desviacion(), 4)
            }
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", tk.END)
            for k, v in self.ultimos_resultados.items():
                self.resultado.insert(tk.END, f"{k}: {v}\n")
            self.resultado.config(state="disabled")
        except ValueError:
            messagebox.showerror("Error", "Solo ingresa números separados por comas.")

    def graficar(self):
        # PROPÓSITO: Muestra una gráfica de barras con los datos ingresados
        if not self.ultimos_datos:
            messagebox.showwarning("Aviso", "Primero calcula algo.")
            return
        plt.figure(figsize=(6, 4))
        plt.bar(range(len(self.ultimos_datos)), self.ultimos_datos, color="steelblue")
        plt.axhline(self.ultimos_resultados["Media"], color="red",
                    linestyle="--", label=f"Media: {self.ultimos_resultados['Media']}")
        plt.title("Gráfica de datos")
        plt.xlabel("Índice")
        plt.ylabel("Valor")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def guardar(self):
        # PROPÓSITO: Guarda los resultados en un archivo JSON
        if not self.ultimos_datos:
            messagebox.showwarning("Aviso", "Primero calcula algo.")
            return
        self.manejador.guardar(self.ultimos_datos, self.ultimos_resultados)
        messagebox.showinfo("Éxito", "Guardado en datos.json")

    def cargar(self):
        # PROPÓSITO: Carga los últimos datos guardados
        contenido = self.manejador.cargar()
        if contenido:
            self.resultado.config(state="normal")
            self.resultado.delete("1.0", tk.END)
            self.resultado.insert(tk.END, f"Datos: {contenido['datos']}\n\n")
            for k, v in contenido["resultados"].items():
                self.resultado.insert(tk.END, f"{k}: {v}\n")
            self.resultado.config(state="disabled")
        else:
            messagebox.showinfo("Info", "No hay datos guardados.")

    def limpiar(self):
        # PROPÓSITO: Limpia la pantalla
        self.entrada.delete(0, tk.END)
        self.resultado.config(state="normal")
        self.resultado.delete("1.0", tk.END)
        self.resultado.config(state="disabled")
        self.ultimos_datos = []
        self.ultimos_resultados = {}

# PROGRAMA PRINCIPAL
ventana = tk.Tk()
app = App(ventana)  # OBJETO: app de la clase App
ventana.mainloop()