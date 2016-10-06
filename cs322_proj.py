#-*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

states = dict()
symbols = []
functions = []
initial = str()
Osymbols = []
Ofunctions = []
# final = []

def newReadline(f):
    return f.readline().strip()

def getDFA():
    fDFA = open("resource/mearly.txt", "r")

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
        Ofunctions.append(dict())

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
    while line != 'Output symbol' and line:
        currS, sym, nextS = line.split(',')
        functions[states[currS]][sym] = nextS
        line = newReadline(fDFA)

    ### read output symbol
    if line != 'Output symbol':
        print 'output symbol not found'
        return 0
    Osymbols = newReadline(fDFA).split(',')

    ### read output function
    line = newReadline(fDFA)
    if line != 'Output function':
        print 'output function not found'
        return 0
    line = newReadline(fDFA)
    while line != 'Initial state' and line:
        currS, sym, printS = line.split(',')
        Ofunctions[states[currS]][sym] = printS
        line = newReadline(fDFA)

    ### read initial state
    if line != 'Initial state':
        print 'initial state not found'
        return 0
    initial = newReadline(fDFA)

    ### read final state
    '''
    line = newReadline(fDFA)
    if line != 'Final state':
        print 'final state not found'
        return 0
    final = newReadline(fDFA).split(',')
    '''

    fDFA.close()
    return (states, symbols, functions, initial, Osymbols, Ofunctions)


def getInput(states, symbols, functions, initial, Osymbols, Ofunctions):
    fInput = open("resource/input.txt", "r")
    fOutput = open("resource/output.txt", "w")

    line = fInput.readline().strip()
    while line != 'end':
        currS = initial
        path = ''

        for al in line:
            try:
                path += Ofunctions[states[currS]][al]
                currS = functions[states[currS]][al]
            except:
                path = 'No path exists!'
                break

        fOutput.write(path)
        fOutput.write('\n')
        line = fInput.readline().strip()

        '''
        if currS in final:
            fOutput.write(u'네')
            fOutput.write('\n')
        else:
            fOutput.write(u'아니요')
            fOutput.write('\n')
        '''

    fInput.close()
    fOutput.close()
    return 0

if __name__ == '__main__':
    DFAres = getDFA()
    if DFAres == 0:
        print 'error while reading DFA'
        sys.exit(1)
    states, symbols, functions, initial, Osymbols, Ofunctions = DFAres


    if getInput(states, symbols, functions, initial, Osymbols, Ofunctions) > 0:
        print 'error while reading input'
        sys.exit(1)
