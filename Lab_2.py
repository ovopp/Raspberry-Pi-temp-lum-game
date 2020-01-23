from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# from gpiozero import MCP3008
import threading
import time
import random
from tkinter import ttk


def setTemp(temp):
    therm["value"] = temp


def plotOnOff():
    global plotVar
    if plotVar:
        plotVar = False
    else:
        plotVar = True


'''Functions for buttons and initializations'''


# Function for plot button
def plotTemperature():
    global plotVar
    while True:
        while plotVar:
            tmpRev = list(reversed(temperatureQueue))
            lumRev = list(reversed(lumQueue))
            color = 'tab:red'
            color2 = 'tab:blue'
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.title("Temperature and Luminescence Plot")
            Ln, = ax.plot(tmpRev)
            ax.set_xlim([0, 10])
            ax.set_ylim([0, 100])
            ax.set_xlabel('Readings')
            ax.set_ylabel('Temperature (*C)', color=color2)
            ax2 = ax.twinx()
            ax2.set_ylabel('Luminescence', color=color)
            ax2.set_ylim([0, 255])
            Ln2, = ax2.plot(lumRev, color=color)
            plt.ion()
            while plotVar:
                plt.show()
                Ln.set_ydata(list(reversed(temperatureQueue)))
                Ln2.set_ydata(list(reversed(lumQueue)))
                Ln.set_xdata(range(len(temperatureQueue)))
                Ln2.set_xdata(range(len(temperatureQueue)))
                plt.pause(0.1)
            plt.close()


# Change the values to values of the photocell and lm 35 data
# Function for daemon Thread to read temperature (will be modified to save photocell / lm 35 data
def getTemp():
    global temperatureQueue
    global lumQueue
    while True:
        while readTemp:
            if len(temperatureQueue) < 10:
                temperatureQueue.insert(0, random.randint(0, 100))
                lumQueue.insert(0, random.randint(0, 255))
            else:
                temperatureQueue.pop()  # Pops the last element
                temperatureQueue.insert(0, random.randint(0,
                                                          100))  # Pushes the first element into Queue, replace with lm35.value
                lumQueue.pop()
                lumQueue.insert(0, random.randint(0, 100))
                setTemp(temperatureQueue[0])
            if celcius:
                tempLabel["text"] = str(temperatureQueue[0]) + " *C"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__()) / len(lumQueue))) + " *C"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / len(lumQueue)))
            else:
                tempLabel["text"] = str(round(temperatureQueue[0] * 1.8 + 32)) + " *F"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__()) / 10)) + " *F"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / 10))
            time.sleep(float(readTime))


# Sets the temperature value on the thermometer
def setTemp(temp):
    therm["value"] = temp


# Initialization function for daemon thread to read values
def __init__():
    thread = threading.Thread(target=getTemp, args=())
    thread.daemon = True
    thread.start()
    thread2 = threading.Thread(target=plotTemperature, args=())
    thread2.daemon = True
    thread2.start()



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
    Label(windowExit, text="Close Program?").grid(row=0, column=1)
    Button(windowExit, text="Yes", command=exit).grid(row=1, column=1, sticky="E")
    Button(windowExit, text="No", command=windowExit.destroy).grid(row=1, column=2, sticky="W")


# Initialization Variables
readTime = 2
readTemp = False
start = False
celcius = True
plotVar = False
temperatureQueue = []
lumQueue = []

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
window.title("Group 20's Temperature and Light Sensor Program")  # sets title

welcome = Label(window, text="Welcome to our program!", fg="blue", font=("Calibri", 25))
start = Label(window, text="To start sensor reading, set a read time \n(default is 2 seconds) and press Start Reading")
blank = Label(window, text="\n\n").grid(row=1, column=1)
currTemp = Label(window, text="Current Temperature: ")
currLum = Label(window, text="Current Luminescence: ")

timeLabel = Label(window, text="Read Time:")
timeEntry = Entry(window)

welcome.grid(row=0, column=2, columnspan=2, padx=5, pady=20)
start.grid(row=2, column=1, sticky="W")
timeLabel.grid(row=3, column=1, sticky="W", padx=5, pady=5)
timeEntry.grid(row=3, column=1, sticky="E", padx=5, pady=5)
currTemp.grid(row=6, column=1, sticky="W", padx=3, pady=3)
currLum.grid(row=7, column=1, sticky="W", padx=3, pady=3)

tempLabel = Label(window, text=" *C")
tempLabel.grid(row=6, column=1, sticky="E", padx=3, pady=3)

lumLabel = Label(window, text=" ")
lumLabel.grid(row=7, column=1, sticky="E", padx=3, pady=3)

convertCF = Button(window, text="C/F", command=celToFah)
convertCF.grid(row=6, column=2, sticky="W", padx=3, pady=3)
getTimeButton = Button(window, text="Set Time", command=getTime)
getTimeButton.grid(row=3, column=2, sticky="W", padx=5, pady=5)

avgTempLabel = Label(window, text="Average Temperature: ")
avgTempLabel.grid(row=8, column=1, sticky="W", padx=3, pady=3)
avgLumLabel = Label(window, text="Average Luminescence: ")
avgLumLabel.grid(row=9, column=1, sticky="W", padx=3, pady=3)

avgTempLabel = Label(window, text="0 *C")
avgTempLabel.grid(row=8, column=1, sticky="E", padx=3, pady=3)
avgLumLabel = Label(window, text="0")
avgLumLabel.grid(row=9, column=1, sticky="E", padx=3, pady=3)

# Thermometer
Label(window, text="50*C/112*F").grid(row=4, column=3, columnspan=2, padx=5, pady=1)  # High temp label
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
therm = ttk.Progressbar(window, style="red.Horizontal.TProgressbar", orient="vertical", length=200, mode="determinate",
                        maximum=4, value=1)  # Progress bar
therm.grid(row=5, rowspan=4, column=3, columnspan=2, padx=1, pady=1)
therm["maximum"] = 50
Label(window, text="0*C/32*F").grid(row=9, column=3, columnspan=2, padx=1, pady=1)  # Low temp label
getTimeButton = Button(window, text="Set Time", command=getTime, width=10).grid(row=1, column=5, padx=5, pady=5)

startTempButton = Button(window, text="Start Reading", command=StartTemp, width=20)
stopTempButton = Button(window, text="Stop Reading", command=stopTemp, width=20)

plotButton = Button(window, text="Plots ON / OFF", command=plotOnOff,
                        width=20)  # Opens a new window for plot data

exitButton = Button(window, text="Exit", command=exit, width=20)

startTempButton.grid(row=4, column=5, padx=5, pady=5)
stopTempButton.grid(row=5, column=5, padx=5, pady=5)
plotButton.grid(row=6, column=5, padx=5, pady=5)  # Opens a new window for plot data
exitButton.grid(row=8, column=5, sticky="W", padx=5, pady=5, columnspan=3)

window.mainloop()
