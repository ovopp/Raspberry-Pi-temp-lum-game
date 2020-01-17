from tkinter import *
import matplotlib matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def start():
    label.config(text = "Start Engaged")

def exit():
    window.destroy()

def plot():
    print("plot things") # do plot things


class GridManagerDemo:
    window = Tk() # create a window
    window.title("Grid Manager Demo") # set title
    message = Message(window, text = "This Message widget occupies three rows and two columns")
    message.grid(row = 1, column = 1, rowspan= 3, columnspan= 2)
    Label(window, text = "First Name:").grid(row = 1, column = 3)
    Entry(window).grid(row = 1, column = 4, padx= 5, pady= 5)
    Label(window, text = "Last Name:").grid(row = 2, column = 3)
    Entry(window).grid(row = 2, column = 4)
    Button(window, text = "Get Name").grid(row = 3, padx= 5, pady= 5, column = 4, sticky = E)
    window.mainloop()

GridManagerDemo()
window = Tk()

# Create a label
label = Label(window, text = "Welcome to Tkinter")
label.pack()

# Create a button
button = Button(window, text  = "Click Me")
button.pack()

# Start Button
button2 = Button(window, text = "Start", command = start)
button2.pack()

# Exit Button
button3 = Button(window, text = "Exit", command = exit)
button3.pack()

# Plot Button
button4 = Button(window, text = "Plot", command = plot)
button4.pack()

# Clear Plot Button
button5 = Button(window, text = "Clear Plot", command = lambda: figCanvas.get_tk_widget().pack_forget())
button5.pack()

fig = Figure(figsize=(5,4))
figCanvas = FigureCanvasTkAgg(fig, master = window)


window.mainloop()
