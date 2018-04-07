
### Define different chess states
EMPTY = 0
BLACK = 1
WHITE = 2

import tkinter
from tkinter import *
import tkinter.font as font
from PIL import Image,ImageTk
import os

def drawBoard(_board):
    lengt = 40
    w_ = 2

    for i in range(19):
        _board.create_line(20, 20 + i * lengt, 20 + 18 * lengt, 20 + i * lengt, width=w_)
        _board.create_line(20 + i * lengt, 20, 20 + i * lengt, 20 + 18 * lengt, width=w_)

    radius = 5
    for i in range(3):
        x_cor_1 = 20 + 3 * lengt
        y_cor_1 = 20 + 3 * lengt + i * 6 * lengt
        for j in range(3):
            x_cor = x_cor_1 + j * 6 * lengt
            y_cor = y_cor_1
            _board.create_oval(x_cor - radius, y_cor - radius, x_cor + radius, y_cor + radius, outline='black',
                                   fill='black')

def start(_window):
    _window.mainloop()

def placeButton(_window):
    labelfont = ('times', 15, 'bold')
    b1 = Button(_window, text="Start",font = labelfont)
    #b1.place(x=800, y=100)
    b1.place(x=810, y=80)

def setMenu(_window):

    # File Menu
    menubar = Menu(_window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open",)
    filemenu.add_command(label="Save",)
    filemenu.add_separator()
    filemenu.add_command(label="Exit",)
    menubar.add_cascade(label="Save the Board", menu=filemenu)


    _window.config(menu=menubar)

###----------------------
### Basic Definition
###----------------------

#absolute path of current folder
dirname = os.path.dirname(__file__)


window = tkinter.Tk()
window.title("Go UI")
window.geometry("980x760+200+30") #900x780 is the size of the window, 200 and 30 is the alignment
window.resizable(width=False,height=False) # Prohibit the resize function

board = tkinter.Canvas(window, width=760, height=760, bg='yellow')
im = ImageTk.PhotoImage(file=dirname + '/source/background.jpg')
board.create_image(0, 200, image=im)
board.grid(row=0, column=0)

#draw line
drawBoard(board)
placeButton(window)
setMenu(window)


if __name__ == '__main__':
    start(window)