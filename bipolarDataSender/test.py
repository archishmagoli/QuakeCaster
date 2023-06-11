from tkinter import *
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np


root = tkinter.Tk()
root.wm_title("Quakecaster Simulator")

btn_forward = tkinter.Button(root, text = "Clockwise")
btn_forward.grid(row = 1, column = 1)

fig = Figure(figsize=(4, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# Creating a label and slider to control the speed of the motor
speedLabel = Label(root, text = "Speed Controls", font=('TkDefaultFont', 15, 'bold'))
descriptionLabel = Label(root, text = "Configure the speed and direction of rotation for your stepper motor below. Press the button for direction (or for \"Stop\") to get your motor running!", wraplength=325, justify="center")
speedLabel.grid(row = 1, column = 0, columnspan = 5)
descriptionLabel.grid(row = 2, column = 0, columnspan = 3)
slider = Scale(root, from_ = 1, to = 10, length = 300, tickinterval = 1, orient=HORIZONTAL)
slider.set(4)
slider.grid(row = 3, column = 0, columnspan = 3)

# Creating the buttons to set the direction of the rotation and transmit this data to the serial
btn_forward = tkinter.Button(root, text = "Clockwise")
btn_forward.grid(row = 8, column = 2, sticky='w')

# btn_backward = tk.Button(root, text = "Anticlockwise", command=RotateAnticlockwise)
# btn_backward.grid(row = 8, column = 1)

btn_stop = tkinter.Button(root, text = "Stop")
btn_stop.grid(row = 8, column = 3)

canvas.get_tk_widget().grid(row = 10, column = 1)

tkinter.mainloop()