from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# from gpiozero import MCP3008
import threading
import time
import random

'''spidev module and code to read'''
# import spidev
# spi = spidev.SpiDev()
# spi.open(0,0)
# spi.max.speed_hz = 5000
# channel = 0
# adc = spi.xfer2([1, (8+channel)<<4,0]) # read from channel 0
# data = ((adc[1]& 3) << 8) + adc[2] # form the 10 bit read value

# photocell = MCP3008(0)
# print(photocell.value)

# lm35 = MCP3000(1)
# print(lm35.value)

'''Functions for buttons and initializations'''


# Function for plot button
def plotTemperature():
    plt.close()
    sum = 0
    for i in temperatureQueue:
        sum += i
    avgTemp = sum / 10
    avgQueue = [avgTemp] * 10
    plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], temperatureQueue)
    plt.ylabel("Temperature (Celcius)")
    plt.xlabel("Last 10 readings")
    plt.title("Temperature Plot")
    plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], avgQueue, label='Average Temperature')
    plt.legend(loc="upper left")
    plt.show()


def plotLuminescence():
    plt.close()
    sum = 0
    for i in lumQueue:
        sum += i
    avgLum = sum / 10
    avgQueue = [avgLum] * 10
    plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], temperatureQueue)
    plt.ylabel("Luminescence (Lum)")
    plt.xlabel("Last 10 readings")
    plt.title("Luminescence Plot")
    plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], avgQueue, label='Average Luminescence')
    plt.legend(loc="upper left")
    plt.show()


# Change the values to values of the photocell and lm 35 data
# Function for daemon Thread to read temperature (will be modified to save photocell / lm 35 data
def getTemp():
    global temperatureQueue
    global lumQueue
    while True:
        while readTemp:
            temperatureQueue.pop()  # Pops the last element
            temperatureQueue.insert(0, random.randint(0,
                                                      100))  # Pushes the first element into Queue, replace with lm35.value
            lumQueue.pop()
            lumQueue.insert(0, random.randint(0, 100))
            if celcius:
                tempLabel["text"] = str(temperatureQueue[0]) + " ℃"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__())/10)) + " ℃"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__())/10))
            else:
                tempLabel["text"] = str(round(temperatureQueue[0] * 1.8 + 32)) + " ℉"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__()) / 10)) + " ℉"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / 10))

            print("Temperature Queue: " + str(temperatureQueue))
            print("Luminescence Queue: " + str(lumQueue))
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


def celToFah():
    global celcius
    if celcius:
        celcius = False
    else:
        celcius = True


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

def exitConfirm():
    windowExit = Tk()
    windowExit.title("Exit Program")
    LabelExit = Label(windowExit, text="Close Program?").grid(row=0, column=1)
    YesButton = Button(windowExit, text="Yes", command=exit).grid(row=1, column=1, sticky="E")
    NoButton = Button(windowExit, text="No", command=windowExit.destroy).grid(row=1, column=2, sticky="W")



# Initialization Variables
readTime = 2
readTemp = False
start = False
celcius = True
temperatureQueue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lumQueue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]




'''Program Starts Here'''
StartWindow = Tk()
StartWindow.geometry("400x600")
StartWindow.title("Group 20's Temperature and Light Sensor Program")
Button(StartWindow, text="Start Program", command=StartProgram, height=20, width=50).pack(padx=5, pady=5)
Button(StartWindow, text="Quit", command=StartWindow.destroy, height=20, width=50).pack(padx=5, pady=5)
StartWindow.mainloop()

if not start:
    quit()  # if user presses Quit instead of Start Program

'''Start of the main program'''

window = Tk()
window.geometry("750x400")
__init__()  # Initializes a daemon thread to read values off sensors (runs in the background, collects data)
matplotlib.use('TkAgg')
window.title("Group 20's Temperature and Light Sensor Program")  # sets title


welcome = Label(window, text="Welcome to our program!", fg = "blue", font=("Calibri", 25))
start = Label(window, text="To start sensor reading, set a read time \n(default is 2 seconds) and press Start Reading")
blank = Label(window, text="\n\n").grid(row=1, column=1)
currTemp = Label(window, text="Current Temperature: ")
currLum = Label(window, text="Current Luminescence: ")

timeLabel = Label(window, text="Read Time:")
timeEntry = Entry(window)

welcome.grid(row=0, column=2, padx=5, pady=20)
start.grid(row=2, column=1, sticky="W")
timeLabel.grid(row=3, column=1, sticky="W", padx=5, pady=5)
timeEntry.grid(row=3, column=1, sticky="E", padx=5, pady=5)
currTemp.grid(row=6, column=1, sticky="W", padx=3, pady=3)
currLum.grid(row=7, column=1, sticky="W", padx=3, pady=3)

tempLabel = Label(window, text=str(temperatureQueue[0]) + " ℃")
tempLabel.grid(row=6, column=1, sticky="E", padx=3, pady=3)

lumLabel = Label(window, text=str(lumQueue[0]))
lumLabel.grid(row=7, column=1, sticky="E", padx=3, pady=3)

convertCF = Button(window, text="C/F", command=celToFah)
convertCF.grid(row=6, column=2, sticky="W", padx=3, pady=3)
getTimeButton = Button(window, text="Set Time", command=getTime)
getTimeButton.grid(row=3, column=2, sticky="W", padx=5, pady=5)

avgTempLabel = Label(window, text="Average Temperature: ")
avgTempLabel.grid(row=8, column=1, sticky="W", padx=3, pady=3)
avgLumLabel = Label(window, text="Average Luminescence: ")
avgLumLabel.grid(row=9, column=1, sticky="W", padx=3, pady=3)


avgTempLabel = Label(window, text="0 ℃")
avgTempLabel.grid(row=8, column=1, sticky="E", padx=3, pady=3)
avgLumLabel = Label(window, text="0")
avgLumLabel.grid(row=9, column=1, sticky="E", padx=3, pady=3)

startTempButton = Button(window, text="Start Reading", command=StartTemp)
stopTempButton = Button(window, text="Stop Reading", command=stopTemp)
plotTempButton = Button(window, text="Temperature Plot", command=plotTemperature)
plotLumButton = Button(window, text="Luminescence Plot", command=plotLuminescence)
exitButton = Button(window, text="Exit", command=exitConfirm, width=20)

startTempButton.grid(row=4, column=5, padx=5, pady=5)
stopTempButton.grid(row=5, column=5, padx=5, pady=5)
plotTempButton.grid(row=6, column=5, padx=5, pady=5)  # Opens a new window for plot data
plotLumButton.grid(row=7, column=5, sticky="W", padx=5, pady=5)
exitButton.grid(row=8, column=5, sticky="W", padx=5, pady=5, columnspan=3)



