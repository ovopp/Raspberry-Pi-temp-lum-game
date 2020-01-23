from tkinter import *
import matplotlib.pyplot as plt
# from gpiozero import MCP3008
import threading
import time
import random
from tkinter import ttk
import csv
import operator

# photocell = MCP3008(0)
# print(photocell.value)

# lm35 = MCP3000(1)
# print(lm35.value)

'''Functions for buttons and initializations'''


def plotOnOff():
    global plotVar
    if plotVar:
        plotVar = False
    else:
        plotVar = True


# Function for plot button
def plotTempandLum():
    global plotVar
    while True:
        try:
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
        except TclError:
            plotVar = False


# Change the values to values of the photocell and lm 35 data
# Function for daemon Thread to read temperature (will be modified to save photocell / lm 35 data
def getTempLum():
    global temperatureQueue
    global lumQueue
    while True:
        while readTemp:
            if len(temperatureQueue) < 10:
                temperatureQueue.insert(0, random.randint(0, 100))
                lumQueue.insert(0, random.randint(0, 255))
                setTemp(temperatureQueue[0])
                setLight(lumQueue[0])
            else:
                temperatureQueue.pop()  # Pops the last element
                temperatureQueue.insert(0, random.randint(0,
                                                          100))  # Pushes the first element into Queue, replace with
                # lm35.value
                lumQueue.pop()
                lumQueue.insert(0, random.randint(0, 100))
                setTemp(temperatureQueue[0])
                setLight(lumQueue[0])
            if celcius:
                tempLabel["text"] = str(temperatureQueue[0]) + " *C"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__()) / len(lumQueue))) + " *C"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / len(lumQueue)))
                time.sleep(float(readTime))
            else:
                tempLabel["text"] = str(round(temperatureQueue[0] * 1.8 + 32)) + " *F"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__()) / len(lumQueue))) + " *F"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / len(lumQueue)))
                time.sleep(float(readTime))


# Sets the temperature value on the thermometer
def setTemp(temp):
    therm["value"] = temp


# Sets the light level on the light meter
def setLight(lightLevel):
    lightMeter["value"] = lightLevel


# Initialization function for daemon thread to read values
def __init__():
    thread = threading.Thread(target=getTempLum, args=())
    thread.daemon = True
    thread.start()
    thread2 = threading.Thread(target=plotTempandLum, args=())
    thread2.daemon = True
    thread2.start()


# Function to open game window
def startGame():
    def submitScore():
        with open('HighScore.csv', 'a') as file:
            file.write("\n" + str(entry.get()) + "," + str(score))
        file.close()
        UpdateLeaderboard()

    def countdown(t):
        countdownLabel['text'] = t
        if t > 0:
            GameMainWindow.after(100, countdown, round(t - 0.1, 1))
        else:
            countdownLabel['text'] = "Time's Up!"

    def UpdateLeaderboard():
        with open('HighScore.csv', 'r') as readHighScore:
            csv1 = csv.reader(readHighScore, delimiter=",")
            sort = sorted(csv1, key=lambda x: int(x[1]), reverse=True)
            highscorerank = 0
            for row in sort:
                Label(GameMainWindow, text=str(row[0]), padx=5, pady=5).grid(row=3 + highscorerank, column=3, sticky="W")
                Label(GameMainWindow, text=str(row[1]), padx=5, pady=5).grid(row=3 + highscorerank, column=3, sticky="E")
                highscorerank += 1
                if highscorerank >= 5:
                    break

    GameMainWindow = Tk()
    GameMainWindow.geometry("800x400")
    GameMainWindow.title("Game")
    score = 0
    countdownTime = 10

    # Game instructions
    InstructionLabel = Label(GameMainWindow, text="INSTRUCTIONS", padx=5, pady=5, width=20, height=3)
    InstructionLabel.grid(row=1, column=1)

    Instruction1 = Label(GameMainWindow, text="You will be given a task you must accomplish in a specified time",
                         padx=5, pady=5)
    Instruction1.grid(row=2, column=1, sticky="W")

    Instruction2 = Label(GameMainWindow,
                         text="If you complete the task your score will be increased and the next task will become harder",
                         padx=5, pady=5)
    Instruction2.grid(row=3, column=1, sticky="W")

    Instruction3 = Label(GameMainWindow,
                         text="If you don't complete the task your game will end and your score will be added to the leaderboard if it is high enough",
                         padx=5, pady=5)
    Instruction3.grid(row=4, column=1, sticky="W")

    Instruction4 = Label(GameMainWindow,
                         text="Possible tasks are: getting the temperature above or below a certain value or getting the light level above or below a certain value",
                         padx=5, pady=5)
    Instruction4.grid(row=5, column=1, sticky="W")

    Instruction5 = Label(GameMainWindow, text="Press start to begin", padx=5, pady=5)
    Instruction5.grid(row=6, column=1, sticky="W")

    # Start and quit button
    gameStartButton = Button(GameMainWindow, text="Start", command=startLevel, width=20, height=3)
    gameStartButton.grid(row=1, column=2, padx=5, pady=5)

    quitGameButton = Button(GameMainWindow, text="Quit", command=quitGame, width=20, height=3)
    quitGameButton.grid(row=2, column=2, padx=5, pady=5)

    # Highscores
    HighscoreLabel = Label(GameMainWindow, text="HIGH SCORES", padx=5, pady=5, width=20, height=3)
    HighscoreLabel.grid(row=1, column=3)

    highscores = [5, 5, 5, 5, 5]
    Label(GameMainWindow, text="Name", padx=5, pady=5).grid(row=2, column=3, sticky="W")
    Label(GameMainWindow, text="Score", padx=5, pady=5).grid(row=2, column=3, sticky="E")
    UpdateLeaderboard()
    
    # Countdown Module
    countdownLabel = Label(GameMainWindow, text=countdownTime)
    countdownLabel.grid()
    Button(GameMainWindow, text="Countdown Start!", command=lambda: countdown(countdownTime)).grid()
    entry = Entry(GameMainWindow)
    entry.grid()
    Button(GameMainWindow, text="Submit Score", command=submitScore).grid()

    GameMainWindow.mainloop()


# Starts next game level
def startLevel():
    return


def quitGame():
    return


# Function to start and stop daemon thread readout
def StartTemp():
    global readTemp
    readTemp = True


def stopTemp():
    global readTemp
    readTemp = False


def celToFah():
    global celcius
    # if ce
    if celcius:
        celcius = False
        highTempLabel["text"] = "112 *F"
        lowTempLabel["text"] = "32 *F"
        tempLabel["text"] = str(round(temperatureQueue[0] * 1.8 + 32)) + " *F"
        avgTempLabel["text"] = str(round(1.8 * sum(temperatureQueue.__iter__()) / 10 + 32)) + " *F"
    else:
        celcius = True
        highTempLabel["text"] = "50 *C"
        lowTempLabel["text"] = "0 *C"
        tempLabel["text"] = str(temperatureQueue[0]) + " *C"
        avgTempLabel["text"] = str(round(sum(temperatureQueue.__iter__()) / 10)) + " *C"


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
plotVar = False
temperatureQueue = [0]
lumQueue = [0]


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
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
window.geometry("800x550")
__init__()  # Initializes two daemon threads to read values off sensors (runs in the background, collects data)
window.title("Group 20's Temperature and Light Sensor Program")  # sets title
for i in range(10):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)

welcome = Label(window, text="Welcome to our program!", fg="blue", font=("Calibri", 25))
welcome.grid(row=0, column=2, columnspan=2, padx=5, pady=20)

start = Label(window, text="To start sensor reading, set a read time \n(default is 2 seconds) and press Start Reading")
start.grid(row=2, column=1, sticky="W")

blank = Label(window, text="\n\n").grid(row=1, column=1)

timeLabel = Label(window, text="Read Time:")
timeLabel.grid(row=3, column=1, sticky="W", padx=5, pady=5)

timeEntry = Entry(window)
timeEntry.grid(row=3, column=1, sticky="E", padx=5, pady=5)

getTimeButton = Button(window, text="Set Time", command=getTime)
getTimeButton.grid(row=3, column=2, sticky="W", padx=5, pady=5)

'''Liminescence'''
# Current luminenscence label
currLum = Label(window, text="Luminescence: ")
currLum.grid(row=4, column=3, padx=3, pady=3)

# Current luminenscence
lumLabel = Label(window, text=" ")
lumLabel.grid(row=7, column=3, sticky="E", padx=60, pady=3)

convertCF = HoverButton(window, text="C/F", command=celToFah)
convertCF.grid(row=6, column=2, sticky="W", padx=3, pady=3)
getTimeButton = HoverButton(window, text="Set Time", command=getTime)
getTimeButton.grid(row=3, column=2, sticky="W", padx=5, pady=5)

# Light meter
Label(window, text="255").grid(row=5, column=3, padx=5, pady=1)  # High temp label
s = ttk.Style()
s.theme_use('clam')
s.configure("yellow.Horizontal.TProgressbar", foreground='black', background='yellow')
lightMeter = ttk.Progressbar(window, style="yellow.Horizontal.TProgressbar", orient="vertical", length=200,
                             mode="determinate", maximum=4, value=1)  # Progress bar
lightMeter.grid(row=6, rowspan=5, column=3, padx=5, pady=1)
lightMeter["maximum"] = 255
Label(window, text="0").grid(row=11, column=3, padx=5, pady=1)  # Low temp label

# Average Luminescence label
avgLumLabel = Label(window, text="Average Luminescence: ")
avgLumLabel.grid(row=12, column=3, sticky="W", padx=10, pady=3)

# Average luminenscence
avgLumLabel = Label(window, text="0")
avgLumLabel.grid(row=12, column=3, sticky="E", padx=10, pady=3)

'''Temperature'''
# Current temperature label
currTemp = Label(window, text="Temperature: ")
currTemp.grid(row=4, column=1, padx=3, pady=3)

# Current temerature
tempLabel = Label(window, text=" *")
tempLabel.grid(row=7, column=1, sticky="E", padx=60, pady=3)

# Thermometer
highTempLabel = Label(window, text="50 *C")  # High temp label
highTempLabel.grid(row=5, column=1, padx=5, pady=1)

s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
therm = ttk.Progressbar(window, style="red.Horizontal.TProgressbar", orient="vertical", length=200, mode="determinate",
                        maximum=4, value=1)  # Progress bar
therm.grid(row=6, rowspan=5, column=1, padx=1, pady=1)
therm["maximum"] = 50

Label(window, text="0*C/32*F").grid(row=9, column=1, columnspan=2, padx=1, pady=1)  # Low temp label

startTempButton = HoverButton(window, text="Start Reading", command=StartTemp, width=20)
startTempButton.grid(row=4, column=5, padx=5, sticky="W", pady=5)

stopTempButton = HoverButton(window, text="Stop Reading", command=stopTemp, width=20)
stopTempButton.grid(row=5, column=5, padx=5, sticky="W", pady=5)

# Opens a new window for plot data
plotButton = HoverButton(window, text="Plots ON / OFF", command=plotOnOff, width=20)
plotButton.grid(row=6, column=5, padx=5, sticky="W", pady=5)

lowTempLabel = Label(window, text="0 *C")  # Low temp label
lowTempLabel.grid(row=11, column=1, padx=1, pady=1)

# Average temperature label
avgTempLabel = Label(window, text="Average Temperature: ")
avgTempLabel.grid(row=12, column=1, sticky="W", padx=3, pady=3)

# Average Temperature
avgTempLabel = Label(window, text="0 *C")
avgTempLabel.grid(row=12, column=1, sticky="E", padx=10, pady=3)

# Game Button

gameButton = Button(window, text="Play a Game!", command=startGame, width=20)
stopTempButton = HoverButton(window, text="Stop Reading", command=stopTemp, width=20)
exitButton = HoverButton(window, text="Exit", command=exitConfirm, width=20)
gameButton.grid(row=7, column=5, sticky="W", padx=5, pady=5, columnspan=3)
exitButton.grid(row=8, column=5, sticky="W", padx=5, pady=5, columnspan=3)

window.mainloop()
