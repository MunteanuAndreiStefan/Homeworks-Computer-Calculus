from tkinter import *
import numpy as np
import math
import sys
import copy
import os
import requests as req

filesURLs = ['https://profs.info.uaic.ro/~ancai/CN/lab/3/a.txt', 'https://profs.info.uaic.ro/~ancai/CN/lab/3/b.txt', 'https://profs.info.uaic.ro/~ancai/CN/lab/3/aplusb.txt', 'https://profs.info.uaic.ro/~ancai/CN/lab/3/aorib.txt']

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

def AddMatrices(firstMatrix, secondMatrix):
    R = copy.deepcopy(firstMatrix)
    for i in range(len(R)):
        nonZeroCol = [j for a, j in R[i]]

        for j in range(len(secondMatrix[i])):
            vB, cB = secondMatrix[i][j]
            if cB in nonZeroCol:
                a = 0.0
                idx = None

                for k in range(len(R[i])):
                    vA = R[i][k][0]
                    cA = R[i][k][1]
                    if cA == cB:
                        a = vA
                        idx = k
                        break

                R[i][idx] = (vA + vB, cB)
            else:
                R[i].append(secondMatrix[i][j])

    return R

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

def MultiplyMatrices(firstMatrix, secondMatrix):
    R = [[] for i in range(len(firstMatrix))]

    for rA in range(len(firstMatrix)):
        for i in range(len(firstMatrix[rA])):

            a, cA = firstMatrix[rA][i]
            for j in range(len(secondMatrix[cA])):

                ok = False
                b, cB = secondMatrix[cA][j]
                r = a * b

                for k in range(len(R[rA])):
                    val = R[rA][k][0]
                    c = R[rA][k][1]
                    if c == cB:
                        ok = True
                        R[rA][k] = (val + r, cB)
                        break

                if not ok:
                    R[rA].append((r, cB))

    return R

def VectorsEqual(firstVector, secondVector, power=5):
    eps = 10 ** (-power)

    if len(firstVector) != len(secondVector):
        print("Lungimea vectorilor nu e aceeasi")
        return False

    for i in range(len(firstVector)):
        if firstVector[i] != secondVector[i]:
            print("Vectori nu sunt egali la indexul {}".format(i))
            return False

    return True

def MatricesEqual(firstMatrix, secondMatrix, power=5):
    eps = 10 ** (-power)

    if len(firstMatrix) != len(secondMatrix):
        print("Nu au acelasi numar de randuri!")
        return False

    for i in range(len(firstMatrix)):
        if len(firstMatrix[i]) != len(secondMatrix[i]):
            print("Coloana nu e egala la {}".format(i))
            return False

        rA = sorted(firstMatrix[i], key = lambda power: power[1])
        rB = sorted(secondMatrix[i], key = lambda power: power[1])

        for j in range(len(rA)):
            if rA[j][1] != rB[j][1]:
                print("Coloana nu e egala la {}{}".format(i, j))
                return False

            if math.fabs(rA[j][0] - rB[j][0]) > eps:
                print("Elementul {} nu e egal cu {}".format(i, j))
                return False

    return True

def ex1():
    A, a = LoadData(filesURLs[0])
    B, b = LoadData(filesURLs[1])
    ApB, z = LoadData(filesURLs[2])
    AmB, t = LoadData(filesURLs[3])

    # Add matrices:
    R = AddMatrices(A, B)
    print("R = A + B?", MatricesEqual(R, ApB))
    val =  "Adunarea matricei A si B:\n" + "R = A + B?\n" + str(MatricesEqual(R, ApB))

    # Multiply matrices
    R = MultiplyMatrices(A, B)
    print("R = A * B", MatricesEqual(R, AmB))
    val += "\n" + "Inmultirea matricei A si B: \n R = A * B \n" + str(MatricesEqual(R, AmB)) + "\n"

    # Multiplying matrix A with vector (2019, 2018, ..., 2, 1)
    x = [float(i) for i in range(2019, 0, -1)]
    r = MultiplyMatrixWithVector(A, x)
    print("r = A * x?", VectorsEqual(r, a))
    val += "Inmultirea matricei A cu vectorul (2019, 2018, ..., 2, 1), r = A * x? \n" + str(VectorsEqual(r, a)) + "\n"

    root = Tk()
    root.title("Ex1")
    root.geometry("350x125")
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