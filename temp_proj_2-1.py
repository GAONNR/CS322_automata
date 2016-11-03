import sys

def main():
    states = list()
    input_symbol = list()
    transitions = dict()
    finals = list()

    get = getENFA(states, input_symbol, transitions, finals)
    states = get[0]
    input_symbol = get[1]
    transitions = get[2]
    initial = get[3]
    finals = get[4]

    closures = getEClosure(states, input_symbol, transitions, initial, finals)

def getENFA(states, input_symbol, transitions, finals):
    f_enfa = open("resource/e-nfa.txt", "r")
    expected_in = ['State', 'Input symbol', 'State transition function', 'Initial state', 'Final state']
    initial = ''

    i = 0
    while i < 5:
        if f_enfa.readline().strip() != expected_in[i]:
            print ('An error occured while reading e-NFA. error number: %s' % expected_in[i])
            sys.exit(1)

        if i == 0:
            states = f_enfa.readline().strip().split(',')
        elif i == 1:
            input_symbol = f_enfa.readline().strip().split(',')
        elif i == 2:
            temp = f_enfa.readline().strip()
            while temp != expected_in[3]:
                try:
                    start, sym, end = temp.split(',')
                except:
                    print ('An error occured while parsing state function: %s' % temp)
                    sys.exit(1)

                if start in transitions:
                    if sym in transitions[start]:
                        transitions[start][sym].append(end)
                    else:
                        transitions[start][sym] = [end]
                else:
                    transitions[start] = dict()
                    transitions[start][sym] = [end]

                temp = f_enfa.readline().strip()

            i += 1
        if i == 3:
            initial = f_enfa.readline().strip()
        elif i == 4:
            finals = f_enfa.readline().strip().split(',')

        i += 1

    return states, input_symbol, transitions, initial, finals

def getEClosure(states, input_symbol, transitions, initial, finals):
    eclosures = []

    for state in states:


if __name__ == '__main__':
    main()
