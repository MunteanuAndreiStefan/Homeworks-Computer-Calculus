from tkinter import *
import numpy as np
import math
import sys
import copy
import os
import requests as req
import random

filesURLs = ['https://profs.info.uaic.ro/~ancai/CN/lab/5/m_rar_sim_2019_500.txt', 'https://profs.info.uaic.ro/~ancai/CN/lab/5/m_rar_sim_2019_1000.txt', 'https://profs.info.uaic.ro/~ancai/CN/lab/5/m_rar_sim_2019_1500.txt', 'https://profs.info.uaic.ro/~ancai/CN/lab/5/m_rar_sim_2019_2019.txt']

def LoadData(url):
    try:
        n, matents = req.get(url).text.split('\r\n\r\n')[:2]
    except:
        print('Datele nu au putut fi preluate de la sursa!')

    try:
        n = int(n)
    except ValueError:
        print('Fisierul nu are un n valid!')
        return False

    A = [[] for i in range(n)]
    for matent in matents.rstrip('\r\n').split('\r\n'):
        a, i, j = matent.split(',')
        A[int(i)].append((float(a), int(j)))

    return A

def MultiplyMatrixWithVector(matrix, vectorAsCol):
    r = []

    for rA in range(len(matrix)):
        vR = 0

        for i in range(len(matrix[rA])):
            vA, colA = matrix[rA][i]
            vX = vectorAsCol[colA]
            vR += vA * vX

        r.append(vR)

    return r

def generateMatrix(nrR, nrC, rare=False):
    if rare:
        A = [[] for i in range(nrR)]

        for i in range(nrR):
            rareC = 7
            cs = [p[1] for p in A[i]]
            js = random.sample([x for x in range(nrC) if x not in cs], rareC)
            ents = [random.uniform(-12.0, 12.0) for _ in range(rareC)]

            for k in range(rareC):
                A[i].append((ents[k], js[k]))
                A[js[k]].append(((ents[k], i)))

        return A
    else:
        A = np.random.uniform(-12.0, 12.0, (nrR, nrC))
        return A

def toPower(matrix, maxK = 1000000, eps = np.finfo(float).eps):
    n = len(matrix)
    v = np.random.randn(n)
    v /= np.linalg.norm(v)

    w = MultiplyMatrixWithVector(matrix, v)
    eigen = np.dot(w, v)
    k = 0

    while True:
        v = w / np.linalg.norm(w)
        w = MultiplyMatrixWithVector(matrix, v)
        eigen = np.dot(w, v)
        k += 1

        if (np.linalg.norm(w - eigen * v) <= n * eps) or (k > maxK):
            break

    if k > maxK:
        raise ValueError("Nu se poate calcula eigenvalue in iteratia: {}".format(maxK))

    return eigen, v

def isSymmetrical(matrix, eps = np.finfo(float).eps):
    for i in range(len(matrix)):
        for a, j in matrix[i]:
            at = None

            for val, k in matrix[j]:
                if k == i:
                    at = val
                    break

            if at is None:  
                return False

            if math.fabs(a - at) > eps: 
                return False

    return True

def ex1():
    resultMsg = ""
    p = int(input("Input p: "))
    n = int(input("Input n: "))

    if p == n:
        if n > 500:
            print('Generarea matricii random: ({n}, {n})...'.format(n=n))
            A = generateMatrix(p, n, rare=True)
            print(isSymmetrical(A))

            try:
                pick = int(input('Selecteaza numarul fisierului pe care vrei sa il incarci:'))
                if pick not in [1, len(filesURLs)]: raise ValueError
            except ValueError:
                print('Alegerea trebuie sa intre 1 si' + str(len(filesURLs)))
                sys.exit(1)

            matrix = LoadData(filesURLs[pick-1])
            v = isSymmetrical(matrix)
            print(v)
            resultMsg += 'Este simetrica: ' +  str(v) +'\n'
            v = toPower(A)[0]
            print(v)
            resultMsg += 'Random: ' + str(v) +'\n'
            v = toPower(matrix)[0]
            print(v)
            resultMsg += 'Matricea selectata: ' + str(v) +'\n'

    elif p > n:

        A = generateMatrix(p, n)
        b = np.random.uniform(-12.0, 12.0, (p,))
        U, S, V = np.linalg.svd(A)

        Spos = S[np.where(S > 0)[0]]
        rank = Spos.size
        invS = np.diag(Spos ** (-1))

        if rank < p:
            invS = np.column_stack((invS, np.zeros((n, p - rank))))
        if rank < n:
            invS = np.row_stack((invS, np.zeros((p, n - rank))))

        invA = np.matmul(np.matmul(V, invS), np.transpose(U))
        invX = np.matmul(invA, b)

        print("Valori singulare:", S)
        print("Rank (SVD):", rank)
        print("Rank (numpy):", np.linalg.matrix_rank(A))
        print("Cond. nr. (SVD):", np.max(S) / np.min(Spos))
        print("Cond. nr. (numpy):", np.linalg.cond(A))
        print("A^I:", invA)
        print("x^I:", invX)

        resultMsg = 'Rank (SVD): ' + str(rank) + '\n' 
        resultMsg += 'Rank (numpy): '  + str(np.linalg.matrix_rank(A)) + '\n' 
        resultMsg += 'Cond. nr. (SVD): ' + str(np.linalg.matrix_rank(A)) + '\n'
        resultMsg += 'Cond. nr. (numpy): ' + str(np.linalg.cond(A)) + '\n'

    if resultMsg is None:
        resultMsg="Nu exista nici o sol pentru p si n."

    root = Tk()
    root.title("Ex1")
    root.geometry("350x250")
    app = Frame(root)
    app.grid()
    label = Label(app, text=resultMsg)
    label.pack(expand=YES, fill=BOTH)
    label.grid()
    root.mainloop()

ex1();