from tkinter import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#from gpiozero import MCP3008
import threading
import time
import random
from tkinter import ttk


def setTemp(temp):
    therm["value"] = temp


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
            setTemp(temperatureQueue[0])
            if celcius:
                tempLabel["text"] = str(temperatureQueue[0]) + " *C"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__())/10)) + " *C"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__())/10))
            else:
                tempLabel["text"] = str(round(temperatureQueue[0] * 1.8 + 32)) + " *F"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__()) / 10)) + " *F"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / 10))

            print("Temperature Queue: " + str(temperatureQueue))
            print("Luminescence Queue: " + str(lumQueue))
            time.sleep(float(readTime))

#Sets the temperature value on the thermometer
def setTemp(temp):
    therm["value"]=temp

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
    Label(windowExit, text="Close Program?").grid(row=0, column=1)
    yes = HoverButton(windowExit, text="Yes", command=exit)
    yes.grid(row=1, column=1, sticky="E")
    no = HoverButton(windowExit, text="No", command=windowExit.destroy)
    no.grid(row=1, column=2, sticky="W")

# Initialization Variables
readTime = 2
readTemp = False
start = False
celcius = True
temperatureQueue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lumQueue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self['activebackground'] = 'light gray'
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

'''Program Starts Here'''
StartWindow = Tk()
StartWindow.geometry("600x480")
StartWindow.title("Group 20's Temperature and Light Sensor Program")
Button(StartWindow, text="Start Program", command=StartProgram, height=20, width=50).pack(padx=5, pady=5)
Button(StartWindow, text="Quit", command=StartWindow.destroy, height=20, width=50).pack(padx=5, pady=5)
StartWindow.mainloop()

if not start:
    quit()  # if user presses Quit instead of Start Program

'''Start of the main program'''

window = Tk()
__init__()  # Initializes a daemon thread to read values off sensors (runs in the background, collects data)
matplotlib.use('TkAgg')
window.title("Group 20's Temperature and Light Sensor Program")  # sets title
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.rowconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.rowconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
window.rowconfigure(4, weight=1)
window.columnconfigure(5, weight=1)
window.rowconfigure(5, weight=1)
window.columnconfigure(6, weight=1)
window.rowconfigure(6, weight=1)
window.columnconfigure(7, weight=1)
window.rowconfigure(7, weight=1)
window.columnconfigure(8, weight=1)
window.rowconfigure(8, weight=1)

welcome = Label(window, text="Welcome to our program!", fg = "blue", font=("Calibri", 25))
welcome.grid(row=0, column=2, columnspan=2, padx=5, pady=20)

start = Label(window, text="To start sensor reading, set a read time \n(default is 2 seconds) and press Start Reading")
start.grid(row=2, column=1, sticky="W")

blank = Label(window, text="\n\n").grid(row=1, column=1)

currTemp = Label(window, text="Current Temperature: ")
currTemp.grid(row=6, column=1, sticky="W", padx=3, pady=3)

currLum = Label(window, text="Current Luminescence: ")
currLum.grid(row=7, column=1, sticky="W", padx=3, pady=3)

timeLabel = Label(window, text="Read Time:")
timeLabel.grid(row=3, column=1, sticky="W", padx=5, pady=5)

timeEntry = Entry(window)
timeEntry.grid(row=3, column=1, sticky="E", padx=5, pady=5)

tempLabel = Label(window, text=str(temperatureQueue[0]) + " *C")
tempLabel.grid(row=6, column=1, sticky="E", padx=3, pady=3)

lumLabel = Label(window, text=str(lumQueue[0]))
lumLabel.grid(row=7, column=1, sticky="E", padx=3, pady=3)

convertCF = HoverButton(window, text="C/F", command=celToFah)
convertCF.grid(row=6, column=2, sticky="W", padx=3, pady=3)
getTimeButton = HoverButton(window, text="Set Time", command=getTime)
getTimeButton.grid(row=3, column=2, sticky="W", padx=5, pady=5)

avgTempLabel = Label(window, text="Average Temperature: ")
avgTempLabel.grid(row=8, column=1, sticky="W", padx=3, pady=3)
avgLumLabel = Label(window, text="Average Luminescence: ")
avgLumLabel.grid(row=9, column=1, sticky="W", padx=3, pady=3)

avgTempLabel = Label(window, text="0 *C")
avgTempLabel.grid(row=8, column=1, sticky="E", padx=3, pady=3)
avgLumLabel = Label(window, text="0")
avgLumLabel.grid(row=9, column=1, sticky="E", padx=3, pady=3)

#Thermometer
Label(window, text="50*C/112*F").grid(row = 4, rowspan=2, column=1, columnspan = 2, padx = 5, pady = 1) #High temp label
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
therm = ttk.Progressbar(window, style="red.Horizontal.TProgressbar", orient="vertical", length=200, mode="determinate", maximum=4, value=1) #Progress bar
therm.grid(row=5, rowspan=4, column=3, columnspan = 2, padx=1, pady=1)
therm["maximum"] = 50
Label(window, text="0*C/32*F").grid(row = 9, column=3, columnspan = 2, padx = 1, pady = 1) #Low temp label

startTempButton = HoverButton(window, text="Start Reading", command=StartTemp, width=20)
startTempButton.grid(row=4, column=5, padx=5, sticky="W", pady=5)

stopTempButton = HoverButton(window, text="Stop Reading", command=stopTemp, width=20)
stopTempButton.grid(row=5, column=5, padx=5, sticky="W", pady=5)

# Opens a new window for plot data
plotTempButton = HoverButton(window, text="Temperature Plot", command=plotTemperature, width=20)
plotTempButton.grid(row=6, column=5, padx=5, sticky="W", pady=5)

stopTempButton = HoverButton(window, text="Stop Reading", command=stopTemp, width=20)
plotLumButton = HoverButton(window, text="Luminescence Plot", command=plotLuminescence, width=20)
plotLumButton.grid(row=7, column=5, sticky="W", padx=5, pady=5)
exitButton = HoverButton(window, text="Exit", command=exitConfirm, width=20)
exitButton.grid(row=8, column=5, sticky="W", padx=5, pady=5, columnspan=3)

window.mainloop()
