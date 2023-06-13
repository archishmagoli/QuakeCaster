from tkinter import *
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

root = tkinter.Tk()
root.wm_title("Quakecaster Simulator")

# Creating a label and slider to control the speed of the motor
speedLabel = Label(root, text = "Speed Controls", font=('TkDefaultFont', 15, 'bold'))
descriptionLabel = Label(root, text = "Configure the speed and direction of rotation for your stepper motor below. Press the button for direction (or for \"Stop\") to get your motor running!", wraplength=325, justify="center")
speedLabel.pack()
descriptionLabel.pack()
slider = Scale(root, from_ = 1, to = 10, length = 300, tickinterval = 1, orient=HORIZONTAL)
slider.set(4)
slider.pack()

# Creating the buttons to set the direction of the rotation and transmit this data to the serial
btn_forward = tkinter.Button(root, text = "Clockwise")
btn_forward.pack(pady=5)

btn_stop = tkinter.Button(root, text = "Stop")
btn_stop.pack(pady=5)

fig = Figure(figsize=(5, 5), dpi=75)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_title("Force Graph (Live)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Force (N)")

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

canvas.get_tk_widget().pack()

root.geometry("400x600")

tkinter.mainloop()