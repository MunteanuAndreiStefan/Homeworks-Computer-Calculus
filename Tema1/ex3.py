from random import uniform
from tkinter import *
import numpy as np
from math import sin, pi
import time

def invFact(n):
    result = 1.0
    for i in range(2, n + 1):
        result = result * 1 / i
    return result

constantValues = [0, invFact(3), invFact(5), invFact(7), invFact(9), invFact(11), invFact(13)]

def P(poly, x):
    xPow3 = x ** 3
    xPow5 = x ** 5
    xPow7 = x ** 7
    xPow9 = x ** 9
    xPow11 = x ** 11
    xPow13 = x ** 13

    if poly == 1:
        return x - constantValues[1] * xPow3 + constantValues[2] * xPow5
    elif poly == 2:
        return x - constantValues[1] * xPow3 + constantValues[2] * xPow5 - constantValues[3] * xPow7
    elif poly == 3:
        return x - constantValues[1] * xPow3 + constantValues[2] * xPow5 - constantValues[3] * xPow7 + constantValues[4] * xPow9
    elif poly == 4:
        return x - 0.166 * xPow3 + 0.00833 * xPow5 - constantValues[3] * xPow7 + constantValues[4] * xPow9
    elif poly == 5:
        return x - constantValues[1] * xPow3 + constantValues[2] * xPow5 - constantValues[3] * xPow7 + constantValues[4] * xPow9 - constantValues[5] * xPow11
    elif poly == 6:
        return x - constantValues[1] * xPow3 + constantValues[2] * xPow5 - constantValues[3] * xPow7 + constantValues[4] * xPow9 - constantValues[5] * xPow11 + constantValues[6] * xPow13
    else:
        return -1001001

def solve1():
    errors = [[0, i] for i in range(0, 7)]
    start = time.time()

    for i in range(0, 10000):
        rv = uniform(-pi / 2, pi / 2)
        for i in range(1, 7):
            error = abs(P(i, rv) - sin(rv))
            errors[i][0] += error

    delta = time.time() - start
    errors = sorted(errors, key=lambda tup: tup[0])
    return (errors[1:7], delta)

def Sol1Msg(errors):
    msg = ''
    for errorTuple in errors:
        msg += 'Eroarea pentru P' + str(errorTuple[1]) + ' este ' + str(errorTuple[0]) + '\n'
    return msg

def P2(poly, x):
    y = x**2
    if poly == 1:
        return x * (1 - y * (constantValues[1] - y * constantValues[2]))
    elif poly == 2:
        return x * (1 - y * (constantValues[1] - y * (constantValues[2] - y * constantValues[3])))
    elif poly == 3:
        return x * (1 - y * (constantValues[1] - y * (constantValues[2] - y * (constantValues[3] - y * constantValues[4]))))
    elif poly == 4:
        return x * (1 - y * (0.166 - y * (0.00833 - y * (constantValues[3] - y * constantValues[4]))))
    elif poly == 5:
        return x * (1 - y * (constantValues[1] - y * (constantValues[2] - y * (constantValues[3] - y * (constantValues[4] - y * constantValues[5])))))
    elif poly == 6:
        return x * (1 - y * (constantValues[1] - y * (constantValues[2] - y * (constantValues[3] - y * (constantValues[4] - y * (constantValues[5] - y * constantValues[6]))))))
    else:
        return -1001001

def solve2():
    errorsAndTimeSolve1 = [[0, 0, i] for i in range(0, 7)]
    errorsAndTimeSolve2 = errorsAndTimeSolve1

    for i in range(0, 100000):
        rv = uniform(-pi / 2, pi / 2)

        for i in range(1, 7):
            timeP1 = time.time()
            valP1 = P(i, rv)
            TfP1 = time.time()
            deltaP1 = TfP1 - timeP1

            error1 = abs(valP1 - sin(rv))
            errorsAndTimeSolve1[i][0] += error1
            errorsAndTimeSolve1[i][1] += deltaP1

            timeP2 = time.time()
            valP2 = P2(i, rv)
            TfP2 = time.time()
            deltaP2 = TfP2 - timeP2

            error2 = abs(valP2 - sin(rv))
            errorsAndTimeSolve2[i][0] += error2
            errorsAndTimeSolve2[i][1] += deltaP2

    errorsAndTimeSolve1 = sorted(errorsAndTimeSolve1, key=lambda tup: tup[0])
    errorsAndTimeSolve2 = sorted(errorsAndTimeSolve2, key=lambda tup: tup[0])

    return (errorsAndTimeSolve1[1:7], errorsAndTimeSolve2[1:7])

def Sol2Msg(errorsAndTimeP1, errorsAndTimeP2):
    msg = ''
    totalTime = 0
    for i in range(0, 6):
        polyNumber = errorsAndTimeP1[i][2]
        errorP1 = errorsAndTimeP1[i][0]
        timeP1 = errorsAndTimeP1[i][1]
        errorP2 = errorsAndTimeP2[i][0]
        timeP2 = errorsAndTimeP2[i][1]
        totalTime = totalTime  + errorsAndTimeP2[i][1]
        msg += 'P' + str(polyNumber) + ' init: ' + 'eroarea:' + str(errorP1) + ' - ' + 'timp:' + str(timeP1) + '\n'
        msg += 'P' + str(polyNumber) + ' nou:  ' + 'eroarea:' + str(errorP2) + ' - ' + 'timp:' + str(timeP2) + '\n'
        msg += '\n   Timp total P2: ' + str(totalTime) + 'ms\n'
    return msg

def ex3():
    root = Tk()

    root.title("Exercitiul 3")
    root.geometry("480x600")

    app = Frame(root)
    app.grid()

    titleLabel = Label(app, text="Partea I")
    titleLabel.grid()
    part1 = solve1()
    errorsPart1 = part1[0]
    deltaPart1 = part1[1]
    textPart1 = "Erorile pentru cele 6 polinoame in cele 10000 numere sunt: \n"
    textPart1 += Sol1Msg(errorsPart1) + "\n"
    textPart1 += "Timp total : " + str(deltaPart1) + "ms\n"
    labelPart1 = Label(app, text=textPart1)
    labelPart1.grid()

    titleLabel2 = Label(app, text="Partea II")
    titleLabel2.grid()
    part2 = solve2()
    errorsAndTimeP1 = part2[0]
    errorsAndTimeP2 = part2[1]
    textPart2 = "    Erorile si timpii pentru cele 6 polinoame (initial si imbunatatit) in 100000 numere sunt: \n"
    textPart2 += Sol2Msg(errorsAndTimeP1, errorsAndTimeP2) + "\n"
    labelPart2 = Label(app, text=textPart2)
    labelPart2.grid()
    root.mainloop()

try:
    ex3()
except:
    print("Ceva eroare.")