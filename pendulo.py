import tkinter as tk
import math

class PendulumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Péndulo Interactivo")

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.angle = 45  # Ángulo inicial del péndulo en grados
        self.length = 100  # Longitud del péndulo
        self.gravity = 9.81  # Gravedad
        self.time_period = 0

        self.angle_label = tk.Label(root, text="Ángulo inicial (grados):")
        self.angle_label.pack()
        self.angle_entry = tk.Entry(root)
        self.angle_entry.pack()

        self.operating_angle_label = tk.Label(root, text="Ángulo de operación (grados):")
        self.operating_angle_label.pack()
        self.operating_angle_entry = tk.Entry(root)
        self.operating_angle_entry.pack()

        self.gravity_label = tk.Label(root, text="Gravedad (m/s^2):")
        self.gravity_label.pack()
        self.gravity_entry = tk.Entry(root)
        self.gravity_entry.pack()

        self.start_button = tk.Button(root, text="Iniciar", command=self.start_pendulum)
        self.start_button.pack()

    def start_pendulum(self):
        try:
            self.angle = float(self.angle_entry.get())
            self.operating_angle = float(self.operating_angle_entry.get())
            self.gravity = float(self.gravity_entry.get())
        except ValueError:
            return

        self.time_period = 2 * math.pi * math.sqrt(self.length / self.gravity)
        self.update_pendulum()

    def update_pendulum(self):
        self.canvas.delete("all")

        # Calcular la posición del péndulo
        t = self.time_period
        angle_rad = math.radians(self.angle)
        x = 200 + self.length * math.sin(angle_rad)
        y = 200 + self.length * math.cos(angle_rad)

        # Dibujar el péndulo
        self.canvas.create_line(200, 200, x, y, width=2, fill="blue")
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")

        # Actualizar el ángulo
        self.angle += 1
        if self.angle > self.operating_angle:
            self.angle = self.operating_angle

        # Llamar a la función de actualización nuevamente después de 10 ms
        self.root.after(10, self.update_pendulum)

if __name__ == "__main__":
    root = tk.Tk()
    app = PendulumApp(root)
    root.mainloop()
