import requests as req
import numpy as np
import sys
import copy
import math
import os
from tkinter import *

filesURLs=['http://profs.info.uaic.ro/~ancai/CN/lab/4/m_rar_2019_1.txt', 'http://profs.info.uaic.ro/~ancai/CN/lab/4/m_rar_2019_2.txt', 'http://profs.info.uaic.ro/~ancai/CN/lab/4/m_rar_2019_3.txt', 'http://profs.info.uaic.ro/~ancai/CN/lab/4/m_rar_2019_4.txt', 'http://profs.info.uaic.ro/~ancai/CN/lab/4/m_rar_2019_5.txt']

#From 3th homework: 
def LoadData(url):
    try:
        n, matents, vecents = req.get(url).text.split('\r\n\r\n')[:3]
    except:
        print('Datele nu au putut fi preluate de la sursa!')

    try:
        n = int(n)
    except:
        print('Fisierul nu are un n valid!')
        return False

    A = [[] for i in range(n)]
    x = []

    for matent in matents.rstrip('\r\n').split('\r\n'):
        a, i, j = matent.split(',')
        A[int(i)].append((float(a), int(j)))

    for vecent in vecents.split('\r\n'):
        a = float(vecent)
        x.append(a)

    return A, x

def MultiplyMatrixWithVector(matrix, vector):
    result = []

    for rA in range(len(matrix)):
        valR = 0

        for i in range(len(matrix[rA])):
            vA, cA = matrix[rA][i]
            valX = vector[cA]
            valR += vA * valX

        result.append(valR)
    return result

def VectorsEqual(firstVector, secondVector, power=5):
    eps = 10 ** (-power)

    if len(firstVector) != len(secondVector):
        print("Lungimea vectorilor nu e aceeasi")
        return False

    for i in range(len(firstVector)):
         if math.fabs(firstVector[i] - secondVector[i])>eps: #modified condition
            print("Vectori nu sunt egali la indexul {}".format(i))
            return False

    return True

#Homework 4
def isDiagNotZero(A):
    for r in range(len(A)):
        ok = False
        for val, c in A[r]:
            if r == c:
                ok = True
        if not ok:
            return False
    return True

def MultiplyVectors(firstVector, secondVector, till=1000000000):
    r = []
    vR = 0

    if till==None:
        nrElements=len(firstVector)
    else:
        nrElements=till

    for i in firstVector:
        vA, cA = i

        if cA >= till:
            continue

        vX = secondVector[cA]
        vR += vA * vX

    return vR

def MultiplyVectors2(firstVector, secondVector, till=1000000000):
    r = []
    vR = 0

    if till==None:
        nrElements=len(firstVector)
    else:
        nrElements=till

    for i in firstVector:
        vA, cA = i

        if cA <= till:
            continue

        vX = secondVector[cA]
        vR += vA * vX

    return vR

def ex1():
    rezMsg=""
    for file in filesURLs:
        ww=[0.8, 1.0, 1.2]
        print(file)

        print('Citeste matricea A...')
        A, b = LoadData(file)
    
        print("E diagonala 0:")
        print(isDiagNotZero(A))

        for w in ww:
            secondVector=b[:]

            it=0
            while(True):
                for i in range(len(secondVector)):
                    for val, c in A[i]:
                        if i == c:
                            aii=val
                    secondVector[i]=(1 - w) * secondVector[i] + w/ aii * (b[i] - MultiplyVectors(A[i], secondVector, i) - MultiplyVectors2(A[i], secondVector, i))
                
                it+=1

                if VectorsEqual(MultiplyMatrixWithVector(A, secondVector),b,5)==True:
                    print("checked:")
                    for k in range(0,5):
                        print(secondVector[k])
                    print(VectorsEqual(MultiplyMatrixWithVector(A, secondVector), b, 5))
                    break
        
            print("Sor parm:")
            print(w)
            rezMsg+="Sor param: " + str(w) + "\n"

            print("Iteration:")
            print(it)
            rezMsg+="Iteration: " + str(it) +"\n"
        
            rez2=np.array(MultiplyMatrixWithVector(A,secondVector))-np.array(b)
            print(rez2)

            print(np.linalg.norm(rez2,float('inf')))
            rezMsg += str(np.linalg.norm(rez2,float('inf')))

    root = Tk()
    root.title("Ex1")
    root.geometry("300x350")
    app = Frame(root)
    app.grid()
    label = Label(app, text=rezMsg)
    label.pack(expand=YES, fill=BOTH)
    label.grid()
    root.mainloop()

try:
    ex1()
except:
    print("Ceva eroare.")