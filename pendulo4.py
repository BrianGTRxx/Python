# Importar las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk

# Definir las constantes del péndulo
g = 9.81 # gravedad estándar de la Tierra en m/s^2
L = 1 # longitud del péndulo en m
theta0 = np.pi/6 # ángulo inicial del péndulo en radianes
omega0 = 0 # velocidad angular inicial del péndulo en rad/s

# Definir la función que calcula el ángulo del péndulo en función del tiempo
def theta(t):
    # Usar la aproximación de ángulos pequeños para el péndulo ideal
    return theta0 * np.cos(np.sqrt(g/L) * t)

# Definir la función que calcula el período del péndulo en función de la gravedad y la longitud
def periodo(g, L):
    # Usar la fórmula para el período del péndulo ideal
    return 2 * np.pi * np.sqrt(L/g)

# Definir la función que calcula las coordenadas del péndulo en función del ángulo
def coordenadas(theta):
    # Usar trigonometría para obtener las coordenadas x e y del péndulo
    x = L * np.sin(theta)
    y = -L * np.cos(theta)
    return x, y

# Definir la función que actualiza la animación del péndulo
def animar(i):
    # Calcular el ángulo y las coordenadas del péndulo en el instante i
    angulo = theta(i/100)
    x, y = coordenadas(angulo)
    # Actualizar la posición del péndulo y el texto del ángulo y el período
    line.set_data([0, x], [0, y])
    circle.center = (x, y)
    texto_angulo.set_text(f"Ángulo: {np.degrees(angulo):.2f}°")
    texto_periodo.set_text(f"Período: {periodo(g, L):.2f} s")
    return line, circle, texto_angulo, texto_periodo

# Crear una ventana de tkinter para seleccionar la gravedad
ventana = tk.Tk()
ventana.title("Seleccionar gravedad")

# Crear una etiqueta con el título
etiqueta_titulo = tk.Label(ventana, text="Selecciona la gravedad del cuerpo celeste:")
etiqueta_titulo.pack()

# Crear un diccionario con los valores de gravedad de algunos cuerpos celestes en m/s^2
gravedades = {"Sol": 274, "Tierra": 9.81, "Luna": 1.62, "Marte": 3.71}

# Crear una variable para almacenar la opción seleccionada
opcion = tk.StringVar()

# Crear un bucle para crear los botones de radio con las opciones de gravedad
for cuerpo, valor in gravedades.items():
    boton_radio = tk.Radiobutton(ventana, text=cuerpo, variable=opcion, value=valor)
    boton_radio.pack()

# Crear una función que cambia el valor de la gravedad global según la opción seleccionada y cierra la ventana
def cambiar_gravedad():
    global g
    g = float(opcion.get())
    ventana.destroy()

# Crear un botón para confirmar la selección y ejecutar la función anterior
boton_confirmar = tk.Button(ventana, text="Confirmar", command=cambiar_gravedad)
boton_confirmar.pack()

# Iniciar el bucle principal de la ventana de tkinter
ventana.mainloop()

# Crear una figura de matplotlib para mostrar la animación del péndulo
fig = plt.figure()
ax = fig.add_subplot(aspect="equal")


# Crear un texto para mostrar el ángulo del péndulo
texto_angulo = ax.text(0.8, 0.9, "", transform=ax.transAxes)

# Crear un texto para mostrar el período del péndulo
texto_periodo = ax.text(0.8, 0.8, "", transform=ax.transAxes)

# Dibujar el péndulo en su posición inicial
x0, y0 = coordenadas(theta0)
line, = ax.plot([0, x0], [0, y0], lw=3, c="k")
circle = ax.add_patch(plt.Circle((x0, y0), 0.08, fc="b"))

anim = FuncAnimation(fig, animar, frames=1000, interval=10, blit=True)


# Ajustar los límites del eje x e y para que se vea todo el movimiento del pénd