# Needed imports
import tkinter
from tkinter import *
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import subprocess, os, platform
import datetime
import warnings
import serial
import serial.tools.list_ports
import sys

# Detecting the Arduino port
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description  # may need tweaking to match new arduinos
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

# Here we are defining the serial port and opening up before sending data
serialInst = serial.Serial()

portVal = arduino_ports[0]
serialInst.baudrate = 9600
serialInst.port = portVal

serialInst.open()

# Defining the variables we'll use when we interact with the GUI
motRun = "1"
indexA = "A"
indexB = "B"
indexD = "D"
newLine = "\n"

## Defining functions we'll use when we press the button
initial = "Stop"
serialInst.write(initial.encode('utf-8'))

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
titleLabel.grid(row=1, column=5, columnspan=11)
titleLabel.pack_propagate(False)

speedLabel = Label(root, text="Motor Controls", font=('TkDefaultFont', 12, 'bold'))
speedLabel.grid(row=2, column=5, padx = 5)
speedLabel.pack_propagate(False)

descriptionLabel = Label(
    root, text="Configure the speed of your stepper motor using the slider below. You can also start and stop your motor with the buttons next to the slider.", wraplength=1000)
descriptionLabel.grid(row=2, column=6, columnspan=5)
descriptionLabel.pack_propagate(False)

slider = Scale(root, from_=1, to=10, length=300, tickinterval=1, orient=HORIZONTAL)
slider.set(4)
slider.grid(row=3, column=5, columnspan=5)
slider.pack_propagate(False)

# Creating the buttons to set the direction of the rotation and transmit this data to the serial
btn_forward = tkinter.Button(root, text="Start Motor", command=RotateClockwise)
btn_forward.pack_propagate(False)

# btn_backward = tk.Button(root, text = "Anticlockwise", command=RotateAnticlockwise)
btn_stop = tkinter.Button(root, text="Stop Motor", command=Stop)
btn_stop.pack_propagate(False)

btn_forward.grid(row=3, column=9, pady=5, padx=5)
# btn_backward.pack(pady=5)
btn_stop.grid(row=3, column=10, pady=5)

# Creating the plot + graph holder
global data_list
data_list = []
fig = Figure(figsize=(4, 4), dpi=75)
ax = fig.add_subplot()

# Export values to CSV
count = 0
def export_csv():
    global count
    filename = datetime.datetime.now().strftime("QuakeCaster_%Y-%m-%d_%H-%M-%S_Export.csv")
    with (open(filename, 'w')) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (s)', 'Force (N)'])
        for item in data_list:
            writer.writerow([count, item])
            count += 1
        count = 0 # Reset count to 0 after exporting
    csvfile.close()

    # Open CSV file after exporting
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', csvfile.name))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(csvfile.name)
    else:                                   # Linux variants
        subprocess.call(('xdg-open', csvfile.name))
        
# Button to export CSV values
btn_export = tkinter.Button(root, text="Export to .csv", command=export_csv)
btn_export.grid(row=4, column=10, pady=5)
btn_export.pack_propagate(False)

# Placing plot into canvas for rendering
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=5, column=5, columnspan=11, padx=10, pady=10)
canvas.get_tk_widget().pack_propagate(False)

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

    # Limit the data list to 1000 values
    data_list = data_list[-500:]

    # Clear the last frame and draw the next frame
    ax.clear()
    ax.plot(data_list)

    # Format plot
    ax.set_ylim([-10, 10])
    ax.set_title("Force Sensor Reading Live Plot")
    ax.set_ylabel("Force (N)")
    ax.set_xlabel("Time (s)")

# Creating the animation
animation_graph = animation.FuncAnimation(
    fig, animate, frames=100, fargs=(data_list, serialInst)) # interval=1000 is one second apart

# Buttons to control the graph animation
btn_pause = tkinter.Button(root, text="Pause/Resume", command=pause_animation)
btn_restart = tkinter.Button(root, text="Clear", command=restart_animation)
btn_pause.pack_propagate(False)
btn_restart.pack_propagate(False)

# Plot title and description
plotTitle = Label(root, text="Plot Controls", font=('TkDefaultFont', 12, 'bold'))
plotTitle.grid(row=4, column=5, padx=5)
plotTitle.pack_propagate(False)

plotDescription = Label(root, text="Use the buttons to the right to control the data points you record.\n\nIf the graph starts at a force of more than 2 Newtons (and you haven't modified the setup), click the \"Reset\" button on the Arduino for calibration!", wraplength=400, justify="left")
plotDescription.grid(row=4, column=6, columnspan=2)
plotDescription.pack_propagate(False)

btn_pause.grid(row=4, column=8, pady=5)
btn_restart.grid(row=4, column=9, pady=5)

plt.show()

# Window configuration
root.geometry("900x525")
root.resizable(False,False)

# Configuring the main loop and cleaning up as needed
try:
    while 'normal' == root.state():
        root.update()
except Exception as e:
    pause_animation()
    serialInst.write(initial.encode('utf-8'))
    serialInst.close()
    sys.exit(0)