# Needed imports
import tkinter
from tkinter import *
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Defining the variables we'll use in our script
motRun = "1"
indexA = "A"
indexB = "B"
indexD = "D"
newLine = "\n"

# Here we are defining the serial port and opening up before sending data
serialInst = serial.Serial()

portVal = "COM3"
serialInst.baudrate = 9600
serialInst.port = portVal

serialInst.open()

## Defining functions we'll use when we press the button

# Sending data to Serial Port
def sendData(motDir):
    total = ""

    if motDir == "Stop":
        total = motDir
    else:
        total += motRun
        total += indexA

        motSpeedInt = slider.get()
        motSpeed = str(11 - motSpeedInt)
        total += motSpeed
        total += indexB

        total += motDir
        total += indexD

    serialInst.write(total.encode('utf-8'))
    serialInst.write(newLine.encode('utf-8'))

# Enable clockwise and anticlockwise rotation and initiate the transmission of data to Serial
def RotateClockwise():
    motDir = "Clockwise"
    sendData(motDir)

# def RotateAnticlockwise():
#     motDir = "Anticlockwise"
#     sendData(motDir)

def Stop():
    motRun = "Stop"
    sendData(motRun)

# Creating the GUI
root = tkinter.Tk()
root.wm_title("QuakeCaster Simulator")

# Creating a label and slider to control the speed of the motor
titleLabel = Label(root, text="QuakeCaster Simulator", font=('TkDefaultFont', 15, 'bold'))
titleLabel.grid(row=1, column=0, columnspan=2)

speedLabel = Label(root, text="Motor Controls", font=('TkDefaultFont', 12, 'bold'))
speedLabel.grid(row=2, column=0, columnspan=2)

descriptionLabel = Label(
    root, text="Configure the speed of your stepper motor using the slider below. You can also start and stop your motor with the buttons under the slider.", wraplength=350, justify="center")
descriptionLabel.grid(row=3, column=0, columnspan=2)

slider = Scale(root, from_=1, to=10, length=300, tickinterval=1, orient=HORIZONTAL)
slider.set(4)
slider.grid(row=4, column=0, columnspan=2)

# Creating the buttons to set the direction of the rotation and transmit this data to the serial
btn_forward = tkinter.Button(root, text="Start Motor", command=RotateClockwise)
# btn_backward = tk.Button(root, text = "Anticlockwise", command=RotateAnticlockwise)
btn_stop = tkinter.Button(root, text="Stop Motor", command=Stop)

btn_forward.grid(row=5, column=0, pady=5)
# btn_backward.pack(pady=5)
btn_stop.grid(row=5, column=1 ,pady=5)

# Creating the plot + graph holder
global data_list
data_list = []
fig = Figure(figsize=(5, 5), dpi=75)
ax = fig.add_subplot()

# Placing plot into canvas for rendering
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Pausing animation functionality
pause = False
def pause_animation():
    global pause
    pause ^= True

# Restart animation functionality
def restart_animation():
    data_list.clear()

# Animation function
def animate(i, data_list, serialInst):

    # Read data from serial port
    bytes = serialInst.readline()
    string_n = bytes.decode()
    string = string_n.rstrip()
    float_value = float(string)

    # Add x and y to lists
    try:
        if not pause:
            float_value = float(string)
            data_list.append(float_value)
    except:
        pass

    # Limit the data list to 100 values
    data_list = data_list[-100:]

    # Clear the last frame and draw the next frame
    ax.clear()
    ax.plot(data_list)

    # Format plot
    ax.set_ylim([-5, 5])
    ax.set_title("Force Sensor Reading Live Plot")
    ax.set_ylabel("Force (N)")
    ax.set_xlabel("Time (s)")

# Creating the animation
animation_graph = animation.FuncAnimation(
    fig, animate, frames=100, fargs=(data_list, serialInst), interval=1000)

# Buttons to control the graph animation
btn_pause = tkinter.Button(root, text="Pause/Resume", command=pause_animation)
btn_restart = tkinter.Button(root, text="Clear", command=restart_animation)

# Plot title and description
plotTitle = Label(root, text="Plot Controls", font=('TkDefaultFont', 12, 'bold'))
plotTitle.grid(row=7, column=0, columnspan=2)

plotDescription = Label(root, text="Use the buttons below to control the data points you record.", wraplength=350, justify="center")
plotDescription.grid(row=8, column=0, columnspan=2)

btn_pause.grid(row=9, column=0, pady=5)
btn_restart.grid(row=9, column=1, pady=5)

plt.show()

# Window configuration
root.geometry("400x700")

# Configuring the main loop and cleaning up as needed
try:
    while 'normal' == root.state():
        root.update()
except:
    serialInst.close()
