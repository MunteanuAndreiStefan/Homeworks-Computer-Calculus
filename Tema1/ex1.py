from tkinter import *
from pip._internal.utils import logging

def machinePrecision():
    m = -1
    u = 10
    while 1.0 + u != 1.0:
        u = 10 ** m
        m -= 1
    return u

def ex1():
    root = Tk()

    root.title("Ex1")
    root.geometry("180x30")

    app = Frame(root)
    app.grid()

    label = Label(app, text="Precizia masina este u = " + str(machinePrecision()))
    label.grid()

    root.mainloop()

try:
    ex1()
except:
    print("Ceva eroare.")