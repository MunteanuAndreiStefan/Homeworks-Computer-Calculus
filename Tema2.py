from tkinter import *
import scipy
import numpy as np
import math
import sys
import os

def DivisionNotPossible():
    print("Nu se poate face impartirea!")
    sys.exit(1)
    
def luMem(A):
    Ainit = np.copy(A)
    nr = Ainit.shape[0]

    for l in range(nr):
        for i in range(l):
            if np.abs(A[i, i]) > np.finfo(float).eps:
                A[i,l] = (Ainit[i,l] - np.dot(A[i, :i], A[:i, l])) / A[i, i]
            else:
                DivisionNotPossible()

        for i in range(l+1):
            A[l, i] = Ainit[l, i] - np.dot(A[l, :i], A[:i, i])

    return A

def SolveForward(A, B):
    nr = A.shape[0]
    X = np.zeros(nr)
    X[0] = B[0] / A[0, 0]

    for i in range(1, nr):
        if np.abs(A[i, i]) > np.finfo(float).eps:
            X[i] = (B[i] - np.dot(A[i, :i], X[:i])) / A[i, i]
        else:
            DivisionNotPossible()

    return X

def SolveBackward(A, B):
    nr = A.shape[0]
    X = np.zeros(nr)
    X[nr-1] = B[nr-1]

    for i in range(nr-2, -1, -1):
        X[i] = B[i] - np.dot(A[i, i+1:], X[i+1:])

    return X

def solve(A, B, backward=False):
    nr = A.shape[0]
    X = np.zeros(nr)

    if backward:
         n = range(nr-1, -1, -1)
    else:
        n = range(nr)

    for i in n:
        if np.abs(A[i, i]) > np.finfo(float).eps:
            X[i] = (B[i] - np.dot(A[i], X)) / A[i, i]
        else:
            DivisionNotPossible()

    return X

def ex1():
    try:
        n = int(input("Enter n: "))
    except ValueError:
        print("N trebuie sa fie numar!")
        sys.exit(1)

    try:
        pick = int(input(
            """
            Apasa:
            - 1 generare random a matricii
            - 2 alege un fisier
            \n\n
            """
        ))
        if pick not in [1, 2]: raise ValueError
    except ValueError:
        print("Alegerea trebuie sa fie 1 sau 2")
        sys.exit(1)

    A = None
    B = None

    if pick == 1:
        A = np.random.rand(n, n)
        B = np.random.rand(n)
    else:
        filename = input("Path al fisierului: ")
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                lines = f.readlines()

                linesA = lines[:n]
                linesB = lines[n:]

                A = np.genfromtxt(linesA, delimiter=',')

                if len(A.shape) != 2 or A.shape[0] != A.shape[1] != n:
                    print("Matricea A trebuie sa aiba {n} randuri si {n} coloane!".format(n=n))
                    sys.exit(1)

                B = np.genfromtxt(linesB, delimiter=',')
                if len(B.shape) != 1 or B.shape[0] != n:
                    print("Matricea A trebuie sa aiba {n} randuri si o coloana!".format(n=n))
                    sys.exit(1)

    Ainit = np.copy(A)
    luMem(A)

    Ylu = SolveForward(A, B)
    Xlu = SolveBackward(A, Ylu)
    Xlib = np.linalg.solve(Ainit, B)

    detA = np.prod(np.diag(A))

    norm1 = np.linalg.norm(np.matmul(Ainit, Xlu) - B)
    norm2 = np.linalg.norm(Xlu - Xlib)
    
    val = "A: "+"\n"+ str(Ainit) + "\n" + "B: "+ "\n" + str(B) + "\n" + "Alu: " + "\n" +  str(A) +"\n" + "Xlu: " + "\n"  + str(Xlu) + "\n" + "Xlib: " + "\n" + str(Xlib) + "\n" + "|A|: " + "\n" +  str(detA) + "\n" + "norm1: " + "\n" + str(norm1) + "\n" + "norm2: " + "\n" + str(norm2) + "\n"
    
    root = Tk()
    root.title("Ex1")
    root.geometry("450x350")
    app = Frame(root)
    app.grid()
    label = Label(app, text=val)
    label.pack(expand=YES, fill=BOTH)
    label.grid()
    root.mainloop()

try:
    ex1()
except:
    print("Ceva eroare.")