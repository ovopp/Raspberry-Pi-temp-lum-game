from tkinter import *
import matplotlib.pyplot as plt
import threading
import time
import random
from tkinter import ttk
import csv

'''Functions for buttons and initializations'''


# Sets the default global values for the game
def resetGlobals():
    global score
    global level
    score = 0
    level = 1


# Counts down from 3 and then starts the level
def Idle():
    # Moves the number down one (exp. 3->2) and at zero destroys the window and opens the next level
    def idleDown(t):
        global level
        IdleLabel['text'] = t
        if t > 0:
            idle.after(1000, idleDown, t - 1)
        else:
            idle.destroy()
            startLevel()

    idle = Tk()
    idle.geometry('100x100')
    for y in range(10):
        idle.columnconfigure(y, weight=1)
        idle.rowconfigure(y, weight=1)
    IdleLabel = Label(idle, text='3', font=400)
    IdleLabel.pack()
    idleDown(3)


# Turns on or off thd plot (opens/closes)
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
                # Setting up the plot
                tmpRev = list(reversed(temperatureQueue))
                lumRev = list(reversed(lumQueue))
                color = 'tab:red'
                color2 = 'tab:blue'
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.title("Temperature and Luminescence Plot")
                Ln, = ax.plot(tmpRev)
                ax.set_xlim([0, 10])
                ax.set_ylim([0, 50])
                ax.set_xlabel('Readings')
                ax.set_ylabel('Temperature (*C)', color=color2)
                ax2 = ax.twinx()
                ax2.set_ylabel('Luminescence', color=color)
                ax2.set_ylim([0, 255])
                Ln2, = ax2.plot(lumRev, color=color)
                plt.ion()

                # Loops through to find the most recent 10 values
                while plotVar:
                    plt.show()
                    Ln.set_ydata(list(reversed(temperatureQueue)))
                    Ln2.set_ydata(list(reversed(lumQueue)))
                    Ln.set_xdata(range(len(temperatureQueue)))
                    Ln2.set_xdata(range(len(temperatureQueue)))
                    plt.pause(0.1)
                plt.close()

        # If there is an error the plot window is closed
        except TclError:
            plotVar = False


# Change the values to values of the photocell and lm 35 data
# Function for daemon Thread to read temperature (will be modified to save photocell / lm 35 data
def getTempLum():
    global temperatureQueue
    global lumQueue
    while True:
        # Records current temparature and updates units based off of user input
        while readTemp:
            if len(temperatureQueue) < 10:
                # Inserts current values into temperature and luminense queue
                temperatureQueue.insert(0, random.randint(0, 50))
                lumQueue.insert(0, random.randint(0, 255))
                setTemp(temperatureQueue[0])
                setLight(lumQueue[0])
            else:
                # Inserts current values into temperature and luminense queue and pops the last value
                temperatureQueue.pop()  # Pops the last element
                temperatureQueue.insert(0, random.randint(0, 50))  # Pushes the first element into Queue, replace with
                # lm35.value
                lumQueue.pop()
                lumQueue.insert(0, random.randint(0, 255))
                setTemp(temperatureQueue[0])
                setLight(lumQueue[0])

            # Changes the units to those specified by the user
            if celcius:
                tempLabel["text"] = str(temperatureQueue[0]) + " *C"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(
                    round(sum(temperatureQueue.__iter__()) / len([i for i in temperatureQueue if i != 0]))) + " *C"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / len([i for i in lumQueue if i != 0])))
                time.sleep(float(readTime))
            else:
                tempLabel["text"] = str(round(temperatureQueue[0] * 1.8 + 32)) + " *F"
                lumLabel["text"] = str(lumQueue[0])
                avgTempLabel["text"] = str(
                    round(sum(temperatureQueue.__iter__()) / len([i for i in temperatureQueue if i != 0]))) + " *F"
                avgLumLabel["text"] = str(round(sum(lumQueue.__iter__()) / len([i for i in lumQueue if i != 0])))
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
    global score

    # Updates the leaderboard on the main screen
    def UpdateLeaderboard():
        with open('HighScore.csv', 'r') as readHighScore:
            # Reads from readHighScore csv file
            csv1 = csv.reader(readHighScore, delimiter=",")
            sort = sorted(csv1, key=lambda x: int(x[1]), reverse=True)
            highscorerank = 0
            for row in sort:
                Label(GameMainWindow, text=str(row[0]), padx=5, pady=5).grid(row=3 + highscorerank, column=3,
                                                                             sticky="W")
                Label(GameMainWindow, text=str(row[1]), padx=5, pady=5).grid(row=3 + highscorerank, column=3,
                                                                             sticky="E")
                highscorerank += 1
                if highscorerank >= 5:
                    break

    # Exits game
    def quitGame():
        GameMainWindow.destroy()

    # Goes from the main game screen to the 321 screen
    def mainToIdle():
        resetGlobals()
        GameMainWindow.destroy()
        Idle()

    # The elements of the main game window
    GameMainWindow = Tk()
    GameMainWindow.geometry("1000x500")
    GameMainWindow.title("Game")
    for y in range(10):
        GameMainWindow.columnconfigure(y, weight=1)
        GameMainWindow.rowconfigure(y, weight=1)

    # Game instructions
    InstructionLabel = Label(GameMainWindow, text="INSTRUCTIONS", padx=5, pady=5, width=20, height=3)
    InstructionLabel.grid(row=1, column=1)

    Instruction1 = Label(GameMainWindow, text="You will be given a task you must accomplish in a specified time",
                         padx=5, pady=5)
    Instruction1.grid(row=2, column=1)

    Instruction2 = Label(GameMainWindow,
                         text="If you complete the task your score will be increased and the next\n task will become "
                              "harder",
                         padx=5, pady=5)
    Instruction2.grid(row=3, column=1)

    Instruction3 = Label(GameMainWindow,
                         text="If you don't complete the task your game will end and your score\n will be added to "
                              "the leaderboard if it is high enough",
                         padx=5, pady=5)
    Instruction3.grid(row=4, column=1)

    Instruction4 = Label(GameMainWindow,
                         text="Possible tasks are: getting the temperature above or below a certain\n value or "
                              "getting the light level above or below a certain value",
                         padx=5, pady=5)
    Instruction4.grid(row=5, column=1)

    Instruction5 = Label(GameMainWindow, text="Press start to begin", padx=5, pady=5)
    Instruction5.grid(row=6, column=1)

    # Start and quit button
    gameStartButton = Button(GameMainWindow, text="Start", command=mainToIdle, width=20, height=3)
    gameStartButton.grid(row=1, column=2, padx=5, pady=5)

    quitGameButton = Button(GameMainWindow, text="Quit", command=quitGame, width=20, height=3)
    quitGameButton.grid(row=2, column=2, padx=5, pady=5)

    # Highscores
    HighscoreLabel = Label(GameMainWindow, text="HIGH SCORES", padx=5, pady=5, width=20, height=3)
    HighscoreLabel.grid(row=1, column=3)
    Label(GameMainWindow, text="Name", padx=5, pady=5).grid(row=2, column=3, sticky="W")
    Label(GameMainWindow, text="Score", padx=5, pady=5).grid(row=2, column=3, sticky="E")
    UpdateLeaderboard()

    GameMainWindow.mainloop()

    # If the player successfully completes the task then the success window opens


def success():
    global score
    global level

    # Goes to the next level
    def continueGame():
        global level
        level += 1
        SuccessWindow.destroy()
        Idle()

    # Exits the success window
    def quitGame():
        SuccessWindow.destroy()
        Fail()
    # Creates a new window
    SuccessWindow = Tk()
    SuccessWindow.geometry("400x200")
    SuccessWindow.title("SUCCESS")

    # Makes the window scalable
    for x in range(10):
        SuccessWindow.columnconfigure(x, weight=1)
        SuccessWindow.rowconfigure(x, weight=1)

    # Original score
    Label(SuccessWindow, text="Score:", width=20).grid(row=2, column=1)
    Label(SuccessWindow, text=str(score)).grid(row=2, column=2, sticky="W")

    # Added score
    Label(SuccessWindow, text="+").grid(row=3, column=1, sticky="E")
    Label(SuccessWindow, text=str(level * 10)).grid(row=3, column=2, sticky="W")

    # Final score
    score += level * 10
    Label(SuccessWindow, text=str(score)).grid(row=4, column=2, sticky="W")

    # Continue and quit buttons
    continueButton = Button(SuccessWindow, text="Continue", command=continueGame, width=20)
    continueButton.grid(row=5, column=1, padx=5, pady=5)

    quitGameButton = Button(SuccessWindow, text="Quit", command=quitGame, width=20)
    quitGameButton.grid(row=5, column=2, padx=5, pady=5)


# Player loses the game
# Supports storing the score, retry & quit game option
def Fail():
    # Stores the score of the player
    def submitScore():
        with open('HighScore.csv', 'a') as file:
            file.write("\n" + str(nameentry.get()) + "," + str(score))
        file.close()
        submitButton.destroy()
        nameentry.destroy()
        Label(failwindow, text="Submitted!").grid(row=0, column=2, sticky='w')

    # Jumps from fail to idle if the user retries
    def failToIdle():
        resetGlobals()
        failwindow.destroy()
        Idle()

    # Goes back to the main game screen if the user decides to quit
    def failToMain():
        failwindow.destroy()
        startGame()

    failwindow = Tk()
    failwindow.geometry("600x200")
    failwindow.title("Lose!")

    for z in range(10):
        failwindow.columnconfigure(z, weight=1)
        failwindow.rowconfigure(z, weight=1)

    # enter player name and submit their score
    nameLabel = Label(failwindow, text="Enter your Name: ")
    nameLabel.grid(row=0, column=1, padx=10)
    nameentry = Entry(failwindow)
    nameentry.grid(row=0, column=2, sticky="W")
    submitButton = HoverButton(failwindow, text="Submit Score", command=submitScore)
    submitButton.grid(row=0, column=3, sticky="W")

    # blank line to allow space between widgets
    Label(failwindow, text="\n").grid(row=1, column=0)

    # restart game
    retryLabel = HoverButton(failwindow, text="Retry", command=failToIdle, width=20)
    retryLabel.grid(row=2, column=1, sticky="W")
    # quit game
    quitLabel = HoverButton(failwindow, text="Quit", command=failToMain, width=20)
    quitLabel.grid(row=2, column=2, sticky="E")


# Starts next game level
def startLevel():
    # Runs the countdown on the level and checks whether the user has completed the task
    def countdown(t):
        countdownLabel['text'] = t
        if tasktype:
            currentLum = random.randint(0, 255)
            currLumGame1['text'] = str(currentLum)

            # If the user achieves the target the success window is opened
            if t > 0:
                if abs(currentLum - randLum) < 2:
                    gamestart.destroy()
                    success()
                else:
                    gamestart.after(100, countdown, round(t - 0.1, 1))

            # If the user runs out of time the fail window is opened
            else:
                gamestart.destroy()
                Fail()
        else:
            currentTemp = random.randint(0, 100)
            currTempGame1['text'] = str(currentTemp)
            # If the user achieves the target the success window is opened
            if t > 0:
                if currentTemp == randTemp:
                    gamestart.destroy()
                    success()
                else:
                    gamestart.after(100, countdown, round(t - 0.1, 1))
            # If the user runs out of time the fail window is opened
            else:
                gamestart.destroy()
                Fail()

    """
    countdowntime represents the allocated time for each stage of the game.


    level represents each stage of the game. Once a stage is cleared, level goes up.
    When a player fails a stage, level gets reset.
    """
    global countdownTime
    global level
    # Generates random target value
    randLum = random.randint(10, 250)
    randTemp = random.randint(15, 19)

    gamestart = Tk()
    gamestart.title("In Game")
    gamestart.geometry('250x100')
    # Scales the box
    for x in range(10):
        gamestart.columnconfigure(x, weight=1)
        gamestart.rowconfigure(x, weight=1)
    # randomly determine the task between Temperature and Luminescence.
    tasktype = random.randint(0, 1)

    # Countdown Module
    countdownLabel = Label(gamestart, text=countdownTime)
    countdownLabel.grid(row=1, column=3, sticky='E')
    countdownLabel1 = Label(gamestart, text="Timer: ")
    countdownLabel1.grid(row=1, column=1, sticky='W')
    if tasktype == 0:
        randLum = 1000  # Blocks false Trues from other task
        goalTemp = Label(gamestart, text="Your goal temperature: ")
        goalTemp.grid(row=2, column=1, padx=3, pady=3, sticky='w')
        goalTemp1 = Label(gamestart, text=randTemp)
        goalTemp1.grid(row=2, column=3, padx=3, pady=3, sticky='e')
        currTempGame = Label(gamestart, text="Temperature: ")
        currTempGame.grid(row=3, column=1, padx=3, pady=3, sticky='w')
        currTempGame1 = Label(gamestart, text=" ")
        currTempGame1.grid(row=3, column=3, padx=3, pady=3, sticky='e')
    else:
        randTemp = 1000  # Blocks false Trues from other task
        goalLum = Label(gamestart, text="Your goal luminescence: ")
        goalLum.grid(row=2, column=1, padx=3, pady=3, sticky='w')
        goalLum1 = Label(gamestart, text=randLum)
        goalLum1.grid(row=2, column=3, padx=3, pady=3, sticky='e')
        currLumGame = Label(gamestart, text="Luminescence: ")
        currLumGame.grid(row=3, column=1, padx=3, pady=3, sticky='w')
        currLumGame1 = Label(gamestart, text=" ")
        currLumGame1.grid(row=3, column=3, padx=3, pady=3, sticky='e')
    # calculates the countdown time
    Label(gamestart, text='Score: ').grid(row=4, column=1, padx=3, pady=3, sticky='w')
    Label(gamestart, text=str(score)).grid(row=4, column=3, padx=3, pady=3, sticky='e')
    Label(gamestart, text='Level: ').grid(row=5, column=1, padx=3, pady=3, sticky='w')
    Label(gamestart, text=str(level)).grid(row=5, column=3, padx=3, pady=3, sticky='e')
    # Countdown time is calculated depending on the level, making it harder as the level goes up.
    # Every time a level goes up, countdown time is reduced by 0.5 seconds.
    if level < 10:
        countdown(round(countdownTime - 0.5 * level, 1))
    else:
        countdown(5)  # Final levels are all 5 seconds


# Function to start and stop daemon thread readout
def StartTemp():
    global readTemp
    readTemp = True


# Stops reading temparature
def stopTemp():
    global readTemp
    readTemp = False


# Coverts the units on the screen from celcius to ferehnheit and vice versa
def celToFah():
    global celcius
    # if *C then it is converted to *F
    if celcius:
        celcius = False
        highTempLabel["text"] = "112 *F"
        lowTempLabel["text"] = "32 *F"
        # equation to convert celcius to farenheit
        tempLabel["text"] = str(round(temperatureQueue[0] * 1.8 + 32)) + " *F"
        avgTempLabel["text"] = str(round(1.8 * sum(temperatureQueue.__iter__()) / 10 + 32)) + " *F"
    # If *F then it is converted to *C
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
            # Returns message confirming the set read time.
            window2.title("Success!")
            Label(window2, text="Valid input!").grid(row=1, column=3, columnspan=5)
            Label(window2, text="The set read time is: " + str(readTime) + " Seconds").grid(row=2, column=3)
            Button(window2, text="Close Window", command=lambda: window2.destroy()).grid(row=3, column=3)
    except ValueError:
        window2 = Tk()
        # Returns warning if the entered set time is not valid.
        window2.title("Warning!")
        Label(window2, text="Invalid input! Please input another number").grid(row=1, column=3)
        Label(window2, text="The current read time is: " + str(readTime) + " Seconds").grid(row=2, column=3)
        Button(window2, text="Close Window", command=lambda: window2.destroy()).grid(row=3, column=3)


# Asks wether the use wants to exit and gives a yes or no button option
def exitConfirm():
    windowExit = Tk()
    windowExit.title("Exit Program")
    Label(windowExit, text="Close Program?").grid(row=0, column=1)
    # Yes Option. Exits the program.
    yes = HoverButton(windowExit, text="Yes", command=exit)
    yes.grid(row=1, column=1, sticky="E")
    # No Option. Returns to the program.
    no = HoverButton(windowExit, text="No", command=windowExit.destroy)
    no.grid(row=1, column=2, sticky="W")


# Initialization Variables and Global Variables
readTime = 2  # default timer for reading time is 2 seconds.s
readTemp = False
start = False
celcius = True
plotVar = False
temperatureQueue = [0]
lumQueue = [0]
countdownTime = 10
# score for the game is initially 0.
score = 0
# level for game play is initially 1.
level = 1


# binds buttons to events (enter & leave)
# code source:
# https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change
class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self['activebackground'] = 'light gray'
        # Binds the button to the event (enter, leave)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # When the cursor enters the button, the color will change to activebackground(light gray)
    def on_enter(self, e):
        self['background'] = self['activebackground']

    # When the cursor leaves the button, the color will change back to its default background.
    def on_leave(self, e):
        self['background'] = self.defaultBackground


'''Start of the main program'''
# Creates new window
window = Tk()
window.geometry("1000x600")
__init__()  # Initializes two daemon threads to read values off sensors (runs in the background, collects data)
window.title("Group 20's Temperature and Light Sensor Program")  # sets title
# sets the weight to each widgets, allowing them to resize accordingly
# as the size of the window changes.
for i in range(10):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)

# Welcome Label.
welcome = Label(window, text="Welcome to our program!", fg="blue", font=("Calibri", 25))
welcome.grid(row=0, column=2, columnspan=2, padx=5, pady=20)

# Information label for setting the timer.
start = Label(window, text="To start sensor reading, set a read time \n(default is 2 seconds) and press Start Reading")
start.grid(row=2, column=1, sticky="W")

# blank label to allow some space between widgets.
blank = Label(window, text="\n\n").grid(row=1, column=1)

# Read Time label
timeLabel = Label(window, text="Read Time:")
timeLabel.grid(row=3, column=1, sticky="W", padx=5, pady=5)

# Entry for time. User enters the timing of how often the sensors are going to be read.
timeEntry = Entry(window)
timeEntry.grid(row=3, column=1, sticky="E", padx=5, pady=5)

# Set Time Button. Sets how often the sensors are read.
getTimeButton = Button(window, text="Set Time", command=getTime)
getTimeButton.grid(row=3, column=2, sticky="W", padx=5, pady=5)

'''Liminescence'''
# Current luminenscence label
currLum = Label(window, text="Luminescence: ")
currLum.grid(row=4, column=3, padx=3, pady=3)

# Current luminenscence
lumLabel = Label(window, text=" ")
lumLabel.grid(row=7, column=3, sticky="E", padx=60, pady=3)

# C/F Button. Converts temperature between Celcius and Farenheit.
convertCF = HoverButton(window, text="C/F", command=celToFah)
convertCF.grid(row=6, column=2, sticky="W", padx=3, pady=3)

# Light meter is a progress bar that displays the current luminescence.
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

# Progress bar that displays the temperature.
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
therm = ttk.Progressbar(window, style="red.Horizontal.TProgressbar", orient="vertical", length=200, mode="determinate",
                        maximum=4, value=1)
therm.grid(row=6, rowspan=5, column=1, padx=1, pady=1)
therm["maximum"] = 50

# Low temp label
Label(window, text="0*C/32*F").grid(row=9, column=1, columnspan=2, padx=1, pady=1)

# Start Reading Button. Starts reading the values from the sensors.
startTempButton = HoverButton(window, text="Start Reading", command=StartTemp, width=20)
startTempButton.grid(row=4, column=5, padx=5, sticky="W", pady=5)

# Stop Reading Button. Stops reading the values from the sensors.
stopTempButton = HoverButton(window, text="Stop Reading", command=stopTemp, width=20)
stopTempButton.grid(row=5, column=5, padx=5, sticky="W", pady=5)

# Opens a new window for plot data
plotButton = HoverButton(window, text="Plots ON / OFF", command=plotOnOff, width=20)
plotButton.grid(row=6, column=5, padx=5, sticky="W", pady=5)

# Low temp label
lowTempLabel = Label(window, text="0 *C")
lowTempLabel.grid(row=11, column=1, padx=1, pady=1)

# Average temperature label
avgTempLabel = Label(window, text="Average Temperature: ")
avgTempLabel.grid(row=12, column=1, sticky="W", padx=3, pady=3)

# Average Temperature
avgTempLabel = Label(window, text="0 *C")
avgTempLabel.grid(row=12, column=1, sticky="E", padx=10, pady=3)

# Game Button
gameButton = Button(window, text="Play a Game!", command=startGame, width=20)
gameButton.grid(row=7, column=5, sticky="W", padx=5, pady=5, columnspan=3)

# Exit Button. Pops up a new window confirming exit.
exitButton = HoverButton(window, text="Exit", command=exitConfirm, width=20)
exitButton.grid(row=8, column=5, sticky="W", padx=5, pady=5, columnspan=3)

window.mainloop()
