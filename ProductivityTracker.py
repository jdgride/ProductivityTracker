"""
Created on Wed Apr  8 15:55:57 2020

@author: John Grider
"""

from pynput import keyboard
from pynput import mouse
from os import getcwd
from time import sleep
from matplotlib import cm
import logging
import win32gui as w
import tkinter as tk
logging.getLogger('matplotlib').setLevel(logging.WARNING)
import matplotlib.pyplot as plt
import numpy as np


log_dir = getcwd()
logging.basicConfig(filename=(log_dir + "/" + "KeyLog.txt"),
                    level=logging.DEBUG, format='%(asctime)s: %(message)s',
                    datefmt='%I:%M')

# Global variables
run = True
name_of_app = ""
Type = {}


# Mouse and keyboard input functions
def on_click(x, y, button, pressed):
    logging.info("Mouse Activity")


def on_scroll(x, y, dx, dy):
    logging.info("Mouse Activity")


def on_move(x, y):
    logging.info("Mouse Activity")


def on_press(key):
    logging.info("Keyboard Activity")
    if str(key) == 'Key.esc':
        global run
        run = False
        print('Exiting...')
        return False


# Button click functions
def work():
    global Type
    Type[name_of_app] = "Work"
    window.destroy()


def browse():
    global Type
    Type[name_of_app] = "Browsing"
    window.destroy()


def leisure():
    global Type
    Type[name_of_app] = "Leisure"
    window.destroy()


## Following code is keyboard, mouse, and app/program listener

# Declare/create listeners for the mouse and keyboard inputs
m_listener = mouse.Listener(on_move=on_move, on_scroll=on_scroll,
                            on_click=on_click)
k_listener = keyboard.Listener(on_press=on_press)
# Start the listeners
m_listener.start()
k_listener.start()
# Hash table for the applications being used
Applications = {}
# Record the time spent on each active window
while (run == True):
    app_name = w.GetWindowText(w.GetForegroundWindow())
    if app_name in Applications:
        Applications[app_name] += 1
    else:
        Applications[app_name] = 1
    sleep(1)

m_listener.stop()

## Following code is data manipulation and visualization

# Open the log file and store into local variables
readFile = open(r"KeyLog.txt", 'r')
lines = readFile.readlines()
readFile.close()
Minutes = {}
for line in lines:
    temp = line.split(" ", 1)
    temp2 = temp[0].strip(":")
    if temp2 in Minutes:
        Minutes[temp2] += 1
    else:
        Minutes[temp2] = 1

temp = []
useless = Applications.pop('', None)
for app in Applications:
    temp.append(app.split("-"))
apps = []
for name in temp:
    if (len(name) > 2):
        apps.append(name[-2:])
    else:
        apps.append(name)

app_names = []
for app in apps:
    app_names.append(app[0].strip())

app_values = []
for app in Applications:
    app_values.append(Applications[app])

Apps = {}
i = 0
for x in range(0, len(app_names)):
    app = app_names[x]
    if app in Apps:
        Apps[app] += app_values[i]
    else:
        Apps[app] = app_values[i]
    i += 1

# Ask the user if each app was for work, browsing, or leisure
for string in Apps:
    name_of_app = string
    window = tk.Tk()
    question = tk.Label(text = "Is " + string + " for work, browsing, or leisure?",
                    fg = "black", bg = "white")
    question.pack()

    workButton = tk.Button(text = "Work", fg = "black", bg = "white", command=work)
    workButton.pack()

    browseButton = tk.Button(text = "Browsing", fg = "black", bg = "white", command=browse)
    browseButton.pack()

    leisureButton = tk.Button(text = "Leisure", fg = "black", bg = "white", command=leisure)
    leisureButton.pack()

    window.mainloop()


######################## Donut chart #########################################
# Get the app names and percentages of each
labels = []
sizes = []
total_time = 0

for app in Apps:
    labels.append(app)
    total_time += Apps[app]
for app in Apps:
    percentage = Apps[app] / total_time
    sizes.append(percentage)

# Set the colors of the chart
num_apps = len(Apps)
cs = cm.Set1(np.arange(num_apps) / num_apps)
# Set the explosion for the chart
explode = (0.05,) * num_apps

plt.pie(sizes, colors=cs, labels=labels, autopct='%1.1f%%',
        startangle=90, pctdistance=0.85, explode=explode)
# draw circle
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')
plt.tight_layout()
plt.show()

####################### Bar Graph #########################################
x = []
y = []
for minute in Minutes:
    x.append(str(minute))
    y.append(Minutes[minute])
y_pos = np.arange(len(x))
plt.bar(x, y, align='center', alpha=0.5)
plt.xticks(y_pos, x)
plt.ylabel('# of Mouse/Keyboard Inputs')
plt.xlabel('Time (Hour:Minute)')
plt.title('Mouse and Keyboard Inputs over Time')

plt.show()

####################### Donut Chart 2 ######################################
labels2 = []
sizes2 = []
Activity = {}

for app in Type:
    if Type[app] in Activity:
        Activity[Type[app]] += Apps[app]
    else:
        Activity[Type[app]] = Apps[app]

for app in Activity:
    labels2.append(app)
    percentage = Activity[app] / total_time
    sizes2.append(percentage)

num_apps = len(Activity)
cs = cm.Set1(np.arange(num_apps) / num_apps)
# Set the explosion for the chart
explode = (0.05,) * num_apps

plt.pie(sizes2, colors=cs, labels=labels2, autopct='%1.1f%%',
        startangle=90, pctdistance=0.85, explode=explode)
# draw circle
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')
plt.tight_layout()
plt.show()
