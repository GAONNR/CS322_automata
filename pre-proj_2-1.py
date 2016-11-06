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

    print (transitions)
    print ('==================')
    closures, new_transitions = getClosure(states, input_symbol, transitions, initial, finals)

def getENFA(states, input_symbol, transitions, finals):
    if len(sys.argv) > 1:
        f_enfa = open(sys.argv[1], "r")
    else:
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

    f_enfa.close()
    return states, input_symbol, transitions, initial, finals

def getClosure(states, input_symbol, transitions, initial, finals):
    closures = []
    closure = set()
    closure.add(initial)
    closure = getEClosure(transitions, closure)
    closures.append(closure)
    idx = -1

    new_transitions = dict()
    while idx < len(closures) - 1:
        idx += 1
        closure = closures[idx]

        for symbol in input_symbol:
            next_closure = set()

            for state in tuple(closure):
                if not (state in transitions):
                    continue
                if not (symbol in transitions[state]):
                    continue
                for state in transitions[state][symbol]:
                    next_closure.update(getEClosure(transitions, set([state])))

            if len(next_closure) > 0:
                chk = True
                for i in range(len(closures)):
                    if closures[i] == next_closure:
                        chk = False
                        break
                if chk == True:
                    closures.append(next_closure)

                if not tuple(closure) in new_transitions:
                    new_transitions[tuple(closure)] = dict()
                new_transitions[tuple(closure)][symbol] = next_closure
                print (str(closure) + ': ' + symbol + ' -> ' + str(next_closure))

    return closures, new_transitions

def getEClosure(transitions, state_set):
    new_set = set()
    chk = True
    while state_set != new_set:
        if chk == False:
            state_set = new_set
        else:
            chk = False
        new_set = set()
        new_set.update(list(state_set))

        for state in tuple(state_set):
            if not (state in transitions):
                continue
            if not ('E' in transitions[state]):
                continue

            new_set.update(transitions[state]['E'])

    return state_set


if __name__ == '__main__':
    main()
