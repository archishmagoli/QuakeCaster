import serial.tools.list_ports
from tkinter import *
import time
import tkinter as tk

# Defining the variables we'll use in our script
motRun = "1"
indexA = "A"
indexB = "B"
indexD = "D"

newLine = "\n"

# Here we are defining the serial port and opening up before sending data
serialInst = serial.Serial()

portVal = "COM3"
print(f"Selecting port {portVal}")

serialInst.baudrate = 9600
serialInst.port = portVal

serialInst.open()

# Functions we'll use when we press the button

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

    confirmTransfer()
    print("Data Sent")

    print(total)


# Showing confirmation message that the data has been sent
def confirmTransfer():
    canvas.itemconfig(confirm_text, text = "Data Sent")
    root.after(1000, confirmTransferReset)

# Resetting the confirmation message
def confirmTransferReset():
    canvas.itemconfig(confirm_text, text = "")

# Functions to enable clockwise and anticlockwise rotation and to initiate the transmission of data to Serial
def RotateClockwise():
    motDir = "Clockwise"
    sendData(motDir)

def RotateAnticlockwise():
    motDir = "Anticlockwise"
    sendData(motDir)

def Stop():
    motRun = "Stop"
    sendData(motRun)

# Defining parameters of GUI and associating GUI widgets
root = Tk()
root.title("QuakeCaster Lab Simulator")

wth = 350
hgt = 300

# Creating the image for the GUI
motor_img = PhotoImage(file = "C:\\Users\\archi\EAS Project\\EAS2600Project\\maxresdefault.png")
canvas = Canvas(width = wth, height = hgt)
canvas.create_image(wth/2, hgt/2, image = motor_img)
canvas.grid(row = 0, column = 0, columnspan = 3)
confirm_text = canvas.create_text(wth/2, hgt/2, text="")

# Creating a label and slider to control the speed of the motor
speedLabel = Label(root, text = "Speed Controls", font=('TkDefaultFont', 15, 'bold'))
descriptionLabel = Label(root, text = "Configure the speed and direction of rotation for your stepper motor below. Press the button for direction (or for \"Stop\") to get your motor running!", wraplength=325, justify="center")
speedLabel.grid(row = 4, column = 0, columnspan = 3)
descriptionLabel.grid(row = 5, column = 0, columnspan = 3)
slider = Scale(root, from_ = 1, to = 10, length = 300, tickinterval = 1, orient=HORIZONTAL)
slider.set(4)
slider.grid(row = 7, column = 0, columnspan = 3)

# Creating the buttons to set the direction of the rotation and transmit this data to the serial
btn_forward = tk.Button(root, text = "Clockwise", command=RotateClockwise)
btn_forward.grid(row = 8, column = 0)

btn_backward = tk.Button(root, text = "Anticlockwise", command=RotateAnticlockwise)
btn_backward.grid(row = 8, column = 1)

btn_stop = tk.Button(root, text = "Stop", command=Stop)
btn_stop.grid(row = 8, column = 2)

# Defining the size of the window and looping through
root.geometry("350x500")
root.mainloop()
