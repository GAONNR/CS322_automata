#-*- coding: utf-8 -*-

import sys

states = dict()
symbols = []
functions = []
initial = str()
final = []

def newReadline(f):
    return f.readline().strip()

def getDFA():
    fDFA = open("resource/dfa.txt", "r")

    ### read state
    line = newReadline(fDFA)
    if line != 'State':
        print 'state not found'
        return 0
    idx = 0
    for state in newReadline(fDFA).split(','):
        states[state] = idx
        idx += 1
        functions.append(dict())

    ### read symbol
    line = newReadline(fDFA)
    if line != 'Input symbol':
        print 'symbol not found'
        return 0
    symbols = newReadline(fDFA).split(',')

    ### read function
    line = newReadline(fDFA)
    if line != 'State transition function':
        print 'function not found'
        return 0
    line = newReadline(fDFA)
    while line != 'Initial state' and line:
        currS, sym, nextS = line.split(',')
        functions[states[currS]][sym] = nextS
        line = newReadline(fDFA)

    ### read initial state
    if line != 'Initial state':
        print 'initial state not found'
        return 0
    initial = newReadline(fDFA)

    ### read final state
    line = newReadline(fDFA)
    if line != 'Final state':
        print 'final state not found'
        return 0
    final = newReadline(fDFA).split(',')

    fDFA.close()
    return (states, symbols, functions, initial, final)


def getInput(states, symbols, functions, initial, final):
    fInput = open("resource/input.txt", "r")
    fOutput = open("resource/output.txt", "w")

    lines = fInput.readlines()
    for i in range(len(lines)):
        currS = initial
        line = lines[i].strip()

        for al in line:
            try:
                currS = functions[states[currS]][al]
            except:
                currS = 'function error'
                break

        if currS in final:
            print u'네'
        else:
            print u'아니요'

    fInput.close()
    fOutput.close()
    return 0

if __name__ == '__main__':
    DFAres = getDFA()
    if DFAres == 0:
        print 'error while reading DFA'
        sys.exit(1)
    states, symbols, functions, initial, final = DFAres


    if getInput(states, symbols, functions, initial, final) > 0:
        print 'error while reading input'
        sys.exit(1)
