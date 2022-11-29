import serial.tools.list_ports
from tkinter import *
import time
import tkinter as tk

# Defining the variables we'll use in our script
motRun = "1"
indexA = "A"
indexB = "B"
indexC = "D"

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
    total += motRun
    total += indexA
    serialInst.write(motRun.encode('utf-8'))
    serialInst.write(indexA.encode('utf-8'))

    motSpeedInt = slider.get()
    motSpeed = str(motSpeedInt)
    total += motSpeed
    total += indexB
    serialInst.write(motSpeed.encode('utf-8'))
    serialInst.write(indexB.encode('utf-8'))

    serialInst.write(motDir.encode())
    serialInst.write(indexC.encode())
    total += motDir
    total += indexC

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
    motRun = 0
    sendData(motRun)

# Defining parameters of GUI and associating GUI widgets
root = Tk()
root.title("Earthquake Simulator GUI")

wth = 350
hgt = 300

# Creating the image for the GUI
motor_img = PhotoImage(file = "C:\\Users\\archi\EAS Project\\EAS2600Project\\maxresdefault.png")
canvas = Canvas(width = wth, height = hgt)
canvas.create_image(wth/2, hgt/2, image = motor_img)
canvas.grid(row = 0, column = 0, columnspan = 2)
confirm_text = canvas.create_text(wth/2, hgt/2, text="")

# Creating a label and slider to control the speed of the motor
speedLabel = Label(root, text = "Speed (in RPM)")
speedLabel.grid(row = 4, column = 0, columnspan = 2)
slider = Scale(root, from_ = 1, to = 9, length = 300, tickinterval = 1, orient=HORIZONTAL)
slider.set(4)
slider.grid(row = 5, column = 0, columnspan = 2)

# Creating the buttons to set the direction of the rotation and transmit this data to the serial
btn_forward = tk.Button(root, text = "Clockwise", command=RotateClockwise)
btn_forward.grid(row = 8, column = 0)

btn_backward = tk.Button(root, text = "Anticlockwise", command=RotateAnticlockwise)
btn_backward.grid(row = 8, column = 1)

# Defining the size of the window and looping through
root.geometry("350x450")
root.mainloop()
