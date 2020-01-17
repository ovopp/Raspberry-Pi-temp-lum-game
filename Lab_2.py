from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# from gpiozero import MCP3008
import logging
import threading
import time

alive = True
readTime = 2


def __init__():
    thread = threading.Thread(target=getTemp, args=())
    thread.daemon = True
    thread.start()


def startTemp():
    global alive
    alive = True


def stopTemp():
    global alive
    alive = False


def getTemp():
    while True:
        while alive:
            print("Temperature is: ")
            time.sleep(float(readTime))


def getTime():
    global readTime
    try:
        tmp = e.get()
        if float(tmp) is not float:
            readTime = tmp
    except ValueError:
        print("invalid input")
    print(readTime)


# photocell = MCP3008(0)
# print(photocell.value)

# lm35 = MCP3000(1)
# print(lm35.value)

matplotlib.use('TkAgg')


def start():
    window.title.config(text="Start Engaged")


def exit():
    window.destroy()


def plot():
    window2 = Tk()
    window2.title("Plot")
    print("plot things")  # do plot things


window = Tk()  # create a window
window.title("Grid Manager Demo")  # set title
message = Message(window, text="This Message widget occupies three rows and two columns")
message.grid(row=1, column=1, rowspan=3, columnspan=2)
Label(window, text="Read Time:").grid(row=1, column=3)
e = Entry(window)
e.grid(row=1, column=4, padx=5, pady=5)
Button(window, text="Get Time", command=getTime).grid(row=1, column=5, padx=5, pady=5)

Label(window, text="Last Name:").grid(row=2, column=3)
Entry(window).grid(row=2, column=4)
Button(window, text="Start Temperature", command=startTemp).grid(row=3, padx=5, pady=5, column=4)
Button(window, text="Stop Temperature", command=stopTemp).grid(row=4, column=4)
fig = Figure(figsize=(5, 4))
figCanvas = FigureCanvasTkAgg(fig, master=window)

# Create a label
label = Label(window, text="Welcome to Tkinter").grid(row=1, column=1)

# Create a button
button = Button(window, text="Click Me").grid(row=5, column=5)

# Start Button
button2 = Button(window, text="Start", command=__init__).grid(row=6, column=5)

# Exit Button
button3 = Button(window, text="Exit", command=exit).grid(row=7, column=5)

# Plot Button
button4 = Button(window, text="Plot", command=plot).grid(row=8, column=5)

# Clear Plot Button
button5 = Button(window, text="Clear Plot", command=lambda: figCanvas.get_tk_widget().pack_forget()).grid(row=10,
                                                                                                          column=5)

window.mainloop()
