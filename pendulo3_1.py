import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
from matplotlib.animation import FuncAnimation

class PendulumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Péndulo Interactivo")

        self.angle = 45  # Ángulo inicial del péndulo en grados
        self.initial_angle = self.angle  # Almacenar el ángulo inicial
        self.length = 100  # Longitud del péndulo
        self.gravity = 9.81  # Gravedad
        self.time_period = 0
        self.period_variation = 0

        self.angle_label = ttk.Label(root, text="Ángulo inicial (grados):")
        self.angle_label.pack()
        self.angle_entry = ttk.Entry(root)
        self.angle_entry.pack()

        self.operating_angle_label = ttk.Label(root, text="Ángulo de operación (grados):")
        self.operating_angle_label.pack()
        self.operating_angle_entry = ttk.Entry(root)
        self.operating_angle_entry.pack()

        self.gravity_label = ttk.Label(root, text="Gravedad (m/s^2):")
        self.gravity_label.pack()
        self.gravity_entry = ttk.Entry(root)
        self.gravity_entry.pack()

        self.period_label = ttk.Label(root, text="Período de oscilación:")
        self.period_label.pack()

        self.period_variation_label = ttk.Label(root, text="Variación de período:")
        self.period_variation_label.pack()

        self.start_button = ttk.Button(root, text="Iniciar", command=self.start_pendulum)
        self.start_button.pack()

        self.reset_button = ttk.Button(root, text="Reiniciar", command=self.reset_pendulum)
        self.reset_button.pack()

        self.create_pendulum_animation()

    def start_pendulum(self):
        try:
            self.angle = float(self.angle_entry.get())
            self.initial_angle = self.angle
            self.operating_angle = float(self.operating_angle_entry.get())
            self.gravity = float(self.gravity_entry.get())
        except ValueError:
            return

        self.time_period = 2 * math.pi * math.sqrt(self.length / self.gravity)
        self.period_label.config(text=f"Período de oscilación: {self.time_period:.2f} segundos")
        self.create_pendulum_animation()

    def pendulum_motion(self, t):
        angle_rad = math.radians(self.angle)
        angular_velocity = math.sqrt(self.gravity / self.length)
        current_angle = angle_rad * math.cos(angular_velocity * t)
        return current_angle

    def update_period(self, i):
        if i == 0:
            self.start_time = 0
            self.start_angle = self.pendulum_motion(0)
        current_time = i * 0.01  # Incremento de tiempo para la animación (más rápido)
        current_angle = self.pendulum_motion(current_time)
        if current_angle * self.start_angle < 0:  # Detecta un cambio de dirección
            new_time = current_time - self.start_time
            self.period_variation = 4 * new_time - self.time_period
            self.time_period = 4 * new_time
            self.period_label.config(text=f"Período de oscilación: {self.time_period:.2f} segundos")
            self.period_variation_label.config(text=f"Variación de período: {self.period_variation:.2f} segundos")
            self.start_time = current_time
            self.start_angle = current_angle

    def reset_pendulum(self):
        self.angle = self.initial_angle
        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, str(self.angle))
        self.period_variation = 0
        self.period_label.config(text=f"Período de oscilación: {self.time_period:.2f} segundos")
        self.period_variation_label.config(text="Variación de período:")
        self.create_pendulum_animation()

    def create_pendulum_animation(self):
        figure = Figure(figsize=(4, 4))
        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        axis = figure.add_subplot(111, aspect="equal")
        axis.set_xlim(-self.length - 10, self.length + 10)
        axis.set_ylim(-self.length - 10, self.length + 10)

        # Dibuja el péndulo
        pendulum_line, = axis.plot([], [], lw=2)
        pendulum_circle = plt.Circle((0, 0), 5, color="red")
        axis.add_patch(pendulum_circle)

        def animate_pendulum(i):
            current_time = i * 0.02  # Incremento de tiempo para la animación (más rápido)
            current_angle = self.pendulum_motion(current_time)
            x = [0, self.length * np.sin(current_angle)]
            y = [0, -self.length * np.cos(current_angle)]
            pendulum_line.set_data(x, y)
            self.update_period(i)
            return pendulum_line,

        # Incrementa el número de cuadros en la animación (más suave)
        animation = FuncAnimation(figure, animate_pendulum, frames=1000, interval=10)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PendulumApp(root)
    root.mainloop()



