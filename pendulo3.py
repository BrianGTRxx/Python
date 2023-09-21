
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
        self.length = 100  # Longitud del péndulo
        self.gravity = 9.81  # Gravedad
        self.time_period = 0

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

        self.start_button = ttk.Button(root, text="Iniciar", command=self.start_pendulum)
        self.start_button.pack()

        self.create_pendulum_animation()

    def start_pendulum(self):
        try:
            self.angle = float(self.angle_entry.get())
            self.operating_angle = float(self.operating_angle_entry.get())
            self.gravity = float(self.gravity_entry.get())
        except ValueError:
            return

        self.time_period = 2 * math.pi * math.sqrt(self.length / self.gravity)
        self.create_pendulum_animation()

    def pendulum_motion(self, t):
        angle_rad = math.radians(self.angle)
        angular_velocity = math.sqrt(self.gravity / self.length)
        current_angle = angle_rad * math.cos(angular_velocity * t)
        return current_angle

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
            current_time = i * 0.05  # Incremento de tiempo para la animación
            current_angle = self.pendulum_motion(current_time)
            x = [0, self.length * np.sin(current_angle)]
            y = [0, -self.length * np.cos(current_angle)]
            pendulum_line.set_data(x, y)
            return pendulum_line,

        animation = FuncAnimation(figure, animate_pendulum, frames=400, interval=50)
        canvas.draw()  # Utiliza draw() en lugar de show()

if __name__ == "__main__":
    root = tk.Tk()
    app = PendulumApp(root)
    root.mainloop()
