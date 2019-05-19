import random
from pip._internal.utils import logging
from ex1 import machinePrecision
from tkinter import *

def checkAssociativityForMultiplication() -> dict:
    x = 5
    u = machinePrecision()
    y = machinePrecision()

    if (x * y) * u != x * (y * u):
        printSolution(x, y, u)

    return \
        {
            'isAssociative': 'False',
            'x': x,
            'y': y,
            'u': u
        }

def printSolution(x : float, y : float, u : float):
    print(" X={v1}\n Y={v2}\n U={v3}".format(v1=x, v2=y, v3=u))
    print("x * (y * u) " + str((x * (y * u))) + "\n")
    print("(x * y) * u " + str(((x * y) * u)) + "\n")

def checkAssociativityForAddition(x: float) -> bool:
    u = machinePrecision()
    return (x + u) + u == x + (u + u)

def getNumberInInterval():
    return random.uniform(0.9, 1), random.uniform(0.9, 1), random.uniform(0.9, 1)

def ex2():
    root = Tk()
    root.geometry("200x100")
    root.title('Ex2')

    app = Frame(root)
    app.pack()

    Label(app, text='Adunarea este asociativa:{resultCheckAsoc}'.format(resultCheckAsoc=checkAssociativityForAddition(1.0))).grid()
    result = checkAssociativityForMultiplication()
    Label(app,
          text='Inmultirea este asocitiva:{isAsoc}\n\n   x={x}\n   y={y}\n   u={u}'.format(
		  isAsoc=result['isAssociative'],
		  x=result['x'], y=result['y'],
		  u=result['u']
		  )).grid()
    root.mainloop()

try:
    ex2()
except:
    print("Ceva eroare.")