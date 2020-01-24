from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time

'''spidev module and code to read'''
import spidev
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 5000

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
            adc = spi.xfer2([1, (8)<<4,0]) # read from channel 0
            data = ((adc[1]& 3) << 8) + adc[2] # form the 10 bit read value
            adc2 = spi.xfer2([1, (9)<<4,0]) # read from channel 0
            data2 = ((adc2[1]& 3) << 8) + adc2[2]
            temperatureQueue.pop()  # Pops the last element
            temperatureQueue.insert(0, round(data2*3.3/1024*100))  # Pushes the first element into Queue, replace with lm35.value
            lumQueue.pop()
            lumQueue.insert(0, round(data/1024*255))
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
message = Message(window, text="Welcome to our program")
message.grid(row=1, column=1, rowspan=2, columnspan=2, padx=1, pady=1)
message1 = Message(window, text="To start sensor reading, set a read time (default is 2 seconds) and press Start "
                                "Reading")
message1.grid(row=3, column=1, rowspan=3, columnspan=2, padx=3, pady=3)

# Get Time Entry window and corresponding button
Label(window, text="Read Time:").grid(row=1, column=3, padx=5, pady=5)
timeEntry = Entry(window)
timeEntry.grid(row=1, column=4, padx=5, pady=5)

Label(window, text="Current Temperature: ").grid(row=6, column=1, padx=3, pady=3)
Label(window, text="Current Luminescence: ").grid(row=7, column=1, padx=3, pady=3)
tempLabel = Label(window, text=str(temperatureQueue[0]) + " ℃")
tempLabel.grid(row=6, column=2, padx=3, pady=3)
lumLabel = Label(window, text=str(lumQueue[0]))
lumLabel.grid(row=7, column=2, padx=3, pady=3)
Button(window, text="C/F", command=celToFah).grid(row=6, column=3, padx=3, pady=3)

Label(window, text="Average Temperature (Over 10 points): ").grid(row=8, column=1, padx=3, pady=3)
Label(window, text="Average Luminescence (Over 10 points): ").grid(row=9, column=1, padx=3, pady=3)
avgTempLabel = Label(window, text="0 ℃")
avgTempLabel.grid(row=8, column=2, padx=3, pady=3)
avgLumLabel = Label(window, text="0")
avgLumLabel.grid(row=9, column=2, padx=3, pady=3)

getTimeButton = Button(window, text="Set Time", command=getTime, width=10).grid(row=1, column=5, padx=5, pady=5)

startTempButton = Button(window, text="Start Reading", command=StartTemp, width=20).grid(row=3, padx=5, pady=5,
                                                                                         column=6)
stopTempButton = Button(window, text="Stop Reading", command=stopTemp, width=20).grid(row=4, column=6, padx=5, pady=5)

plotTempButton = Button(window, text="Temperature Plot", command=plotTemperature, width=20).grid(row=5, column=6,
                                                                                                 padx=5,
                                                                                                 pady=5)  # Opens a new window for plot data
plotLumButton = Button(window, text="Luminescence Plot", command=plotLuminescence, width=20).grid(row=6, column=6,
                                                                                                  padx=5, pady=5)

exitButton = Button(window, text="Exit", command=exit, width=20).grid(row=7, column=6, padx=5, pady=5, columnspan=3)

# Will be a thermometer at some point or another
'''canvas = Canvas(window, width=200, height=500)
canvas.create_rectangle(15, 200, 50, 50)
canvas.grid(column=4)'''

window.mainloop()  # Last line of project

