from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# from gpiozero import MCP3008
import threading
import time
import logging

# photocell = MCP3008(0)
# print(photocell.value)

# lm35 = MCP3000(1)
# print(lm35.value)

'''Functions for buttons and initializations'''


# Function for plot button
def plot():
    window2 = Tk()
    window2.title("Plot")
    print("plot things")  # do plot things


# Function for daemon Thread to read temperature (will be modified to save photocell / lm 35 data
def getTemp():
    while True:
        while readTemp:
            print("Temperature is: ")
            time.sleep(float(readTime))


# Initialization function for daemon thread to read values
def __init__():
    thread = threading.Thread(target=getTemp, args=())
    thread.daemon = True
    thread.start()


# Function to start and stop daemon thread readout
def StartTemp():
    global readTemp
    readTemp = True


def stopTemp():
    global readTemp
    readTemp = False


# Updates readTime variable with Entry information. Throws and handles incorrect inputs
def getTime():
    global readTime
    try:
        tmp = timeEntry.get()
        if float(tmp) is not float:
            readTime = tmp
            window2 = Tk()
            window2.title("Success!")
            Label(window2, text="Valid input!").grid(row=1, column=3, columnspan=5)
            Label(window2, text="The set read time is: " + str(readTime) + " Seconds").grid(row=2, column=3)
            Button(window2, text="Close Window", command=lambda: window2.destroy()).grid(row=3, column=3)
    except ValueError:
        window2 = Tk()
        window2.title("Warning!")
        Label(window2, text="Invalid input! Please input another number").grid(row=1, column=3)
        Label(window2, text="The current read time is: " + str(readTime) + " Seconds").grid(row=2, column=3)
        Button(window2, text="Close Window", command=lambda: window2.destroy()).grid(row=3, column=3)


# Function to destroy and start program for Start Program Button
def StartProgram():
    StartWindow.destroy()
    global start
    start = True


# Initialization Variables
readTime = 2
readTemp = False
start = False

StartWindow = Tk()
Button(StartWindow, text="Start Program", command=StartProgram).pack()
Button(StartWindow, text="Quit", command=StartWindow.destroy).pack()
StartWindow.mainloop()

if not start:
    quit()  # if user presses Quit instead of Start Program

# Starting new window with main program
window = Tk()
__init__()
matplotlib.use('TkAgg')
window.title("Group 20's Temperature and Light Sensor Program")  # sets title
message = Message(window, text="Welcome to the Future")
message.grid(row=1, column=1, rowspan=3, columnspan=2)

# Get Time Entry window and corresponding button
Label(window, text="Read Time:").grid(row=1, column=3)
timeEntry = Entry(window)
timeEntry.grid(row=1, column=4, padx=5, pady=5)

getTimeButton = Button(window, text="Get Time", command=getTime).grid(row=1, column=5, padx=5, pady=5)

startTempButton = Button(window, text="Start Temperature Read", command=StartTemp).grid(row=3, padx=5, pady=5,
                                                                                   column=4)
stopTempButton = Button(window, text="Stop Temperature Read", command=stopTemp).grid(row=4, column=4)

exitButton = Button(window, text="Exit", command=window.destroy).grid(row=7, column=5)

plotButton = Button(window, text="Plot", command=plot).grid(row=8, column=5)

window.mainloop()
