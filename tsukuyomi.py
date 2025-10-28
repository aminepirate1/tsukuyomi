# tsukuyomi.py
# Python 3.x
# Dipendenze: solo la libreria standard (tkinter)
#
# Premi ESC o chiudi la finestra per uscire.

import tkinter as tk
import math
import time
import colorsys

WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = min(WIDTH, HEIGHT) * 0.45
NUM_SPOKES = 120
FPS = 60

class Tsukuyomi:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        self.angle = 0.0
        self.start_time = time.time()
        self.running = True

        # overlay text
        self.title_text = self.canvas.create_text(
            CENTER[0], 60,
            text="TSUKUYOMI INFINITO",
            fill="white",
            font=("Helvetica", 28, "bold")
        )
        self.hint_text = self.canvas.create_text(
            CENTER[0], HEIGHT - 40,
            text="Premi ESC per uscire",
            fill="white",
            font=("Helvetica", 12)
        )

        root.bind("<Escape>", lambda e: self.stop())
        root.protocol("WM_DELETE_WINDOW", self.stop)
        self.frame()

    def stop(self):
        self.running = False
        self.root.destroy()

    def frame(self):
        if not self.running:
            return

        # time-based parameters
        t = time.time() - self.start_time
        self.angle += 0.015 + 0.005 * math.sin(t * 0.6)   # rotazione lenta, variabile
        puls = 0.5 + 0.5 * math.sin(t * 0.8)             # pulsazione 0..1
        twist = math.sin(t * 0.4) * 0.8                  # leggera ondulazione

        self.canvas.delete("spoke")  # rimuove i disegni precedenti

        # disegna raggi ipnotici
        for i in range(NUM_SPOKES):
            a = (i / NUM_SPOKES) * 2 * math.pi
            # applica rotazione + twist
            a2 = a + self.angle + math.sin(i * 0.12 + t * 0.8) * 0.2 * twist

            # lunghezza variabile per effetto ondulatorio
            r = RADIUS * (0.2 + 0.8 * (0.5 + 0.5 * math.cos(i * 0.3 + t * 1.1))))
            x = CENTER[0] + math.cos(a2) * r * (0.6 + 0.4 * puls)
            y = CENTER[1] + math.sin(a2) * r * (0.6 + 0.4 * puls)

            # colore ciclico HSV -> RGB per creare l'effetto rosso/nero/magico
            hue = ((i / NUM_SPOKES) + (t * 0.05)) % 1.0
            # usa tonalità più vicine al rosso/viola per "estetica tsukuyomi"
            h = (0.98 * hue + 0.02) % 1.0
            r_c, g_c, b_c = [int(255 * c) for c in colorsys.hsv_to_rgb(h, 0.8, 0.9)]
            color = f"#{r_c:02x}{g_c:02x}{b_c:02x}"

            # spessore e opacità simulata (opacità non nativa in tkinter)
            width = 1 + 3 * (0.5 + 0.5 * math.sin(i * 0.2 + t * 1.6)) * puls

            # disegna linea dal centro al punto
            self.canvas.create_line(
                CENTER[0], CENTER[1], x, y,
                fill=color, width=width, tag="spoke", smooth=True
            )

        # Cerchi concentrici semitrasparenti (simulati con vari livelli di grigio)
        for j in range(6):
            rr = RADIUS * (0.12 + j * 0.13) * (0.8 + 0.2 * puls)
            stroke = int(40 + 30 * j + 60 * puls)
            stroke = max(0, min(255, stroke))
            col = f"#{stroke:02x}{0:02x}{0:02x}"  # toni scuri-rossastri
            self.canvas.create_oval(
                CENTER[0] - rr, CENTER[1] - rr, CENTER[0] + rr, CENTER[1] + rr,
                outline=col, width=2, tag="spoke"
            )

        # piccolo "occhio" centrale che pulsa
        eye_radius = 16 + 8 * puls
        eye_color = "#ff3333"
        self.canvas.create_oval(
            CENTER[0] - eye_radius, CENTER[1] - eye_radius,
            CENTER[0] + eye_radius, CENTER[1] + eye_radius,
            fill=eye_color, outline="", tag="spoke"
        )

        # schedule next frame
        delay = int(1000 / FPS)
        self.root.after(delay, self.frame)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tsukuyomi Infinito")
    app = Tsukuyomi(root)
    root.mainloop()