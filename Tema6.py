from tkinter import *
import numpy as np
global h

h = 0.00000001
eps = np.finfo(float).eps

j=[42.0, -55.0 , -42.0 ,49.0 , -6.0]
a = np.array(j).astype(int)

A = max(a)
R = (a[0] + A) / a[0]

print(a)

def Pd2(a, x):
    return P(np.polyder(a, 2), x)

def Pd(a, x):
    return P(np.polyder(a), x)

def P(vec, x):
    result = 0
    for i in vec:
        result = result * x + i
    return result

def Solve():
    i=-R
    solutions=[]
    while i<=R:

        maxK=1000
        delta = 1
        x=i
        k = 0

        while (k < maxK):
            A = 2 * Pd(a, x)**2 - P(a, x) * Pd2(a, x)

            if  A<eps: 
                break

            delta = P(a, x) * Pd(a, x) / A
            newX = x - delta

            if abs(delta) <= eps:  
                break

            x = newX
            k+=1

        if delta < eps and abs(P(a, x))<eps*1e4:
            solutions+=[x]
    
        i+=2*R/100

    solutions.sort()
    k=1

    while k < len(solutions):
        if abs(solutions[k]-solutions[k-1])<eps*1e4:
            del solutions[k]
        else:
            k+=1

    print("Solutii:")
    print(solutions)
    return solutions

def ex1():
    val = str(a)+ '\n'
    val += 'Solutii \n' + str(Solve())+ '\n'

    root = Tk()
    root.title("Ex1")
    root.geometry("480x50")
    app = Frame(root)
    app.grid()
    label = Label(app, text=val)
    label.pack(expand=YES, fill=BOTH)
    label.grid()
    root.mainloop()

ex1()