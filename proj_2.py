import sys
import ohmyply

class Myset:
    def __init__(self):
        self.states = list()
        self.input_symbol = list()
        self.transitions = dict()
        self.initial = ''
        self.finals = list()

state_idx = 0

def main():
    re_in = open("resource/re.txt", "r")
    my_input = re_in.readline().strip()
    parsed_tree = ohmyply.parse(my_input)
    ENFAset = parseENFA(parsed_tree)
    ENFAset.input_symbol = list(ohmyply.symbols)
    ENFAset.input_symbol.sort()

    DFAset = Myset()
    DFAset.states, DFAset.transitions = getClosure(ENFAset.states, ENFAset.input_symbol, ENFAset.transitions, ENFAset.initial, ENFAset.finals)
    DFAset.input_symbol = ENFAset.input_symbol
    DFAset.initial = DFAset.states[0]
    for s in DFAset.states:
        chk = False
        for state in ENFAset.finals:
            if state in tuple(s):
                chk = True
                break

        if chk == True:
            DFAset.finals.append(s)

    mDFAset = minimizeDFA(DFAset)
    printResult(mDFAset)

def parseENFA(parsed_tree):
    global state_idx
    whatistype = parsed_tree.classtype
    newENFA = Myset()

    if whatistype == 'Symbol':
        for i in range(4):
            newENFA.states.append(i + state_idx)
        state_idx += 4

        newENFA.initial = newENFA.states[0]
        newENFA.finals.append(newENFA.states[3])

        newENFA.transitions[newENFA.initial] = dict()
        newENFA.transitions[newENFA.initial]['E'] = [newENFA.states[1]]
        newENFA.transitions[newENFA.states[1]] = dict()
        newENFA.transitions[newENFA.states[1]][parsed_tree.value] = [newENFA.states[2]]
        newENFA.transitions[newENFA.states[2]] = dict()
        newENFA.transitions[newENFA.states[2]]['E'] = [newENFA.finals[0]]

    elif whatistype == 'Concat':
        enfa1 = parseENFA(parsed_tree.value[0])
        enfa2 = parseENFA(parsed_tree.value[1])
        newENFA.initial = enfa1.initial
        newENFA.finals.append(enfa2.finals[0])

        newENFA.states = enfa1.states + enfa2.states
        newENFA.transitions.update(enfa1.transitions)
        newENFA.transitions.update(enfa2.transitions)
        if not (enfa1.finals[0] in newENFA.transitions):
            newENFA.transitions[enfa1.finals[0]] = dict()
        if not ('E' in newENFA.transitions[enfa1.finals[0]]):
            newENFA.transitions[enfa1.finals[0]]['E'] = list()
        newENFA.transitions[enfa1.finals[0]]['E'].append(enfa2.initial)

    elif whatistype == 'Star':
        enfa = parseENFA(parsed_tree.value)
        newENFA = enfa
        if not (enfa.finals[0] in newENFA.transitions):
            newENFA.transitions[enfa.finals[0]] = dict()
        if not ('E' in newENFA.transitions[enfa.finals[0]]):
            newENFA.transitions[enfa.finals[0]]['E'] = list()
        enfa.transitions[enfa.initial]['E'].append(enfa.finals[0])
        if not (enfa.finals[0] in enfa.transitions):
            enfa.transitions[enfa.finals[0]] = dict()
        if not ('E' in enfa.transitions[enfa.finals[0]]):
            enfa.transitions[enfa.finals[0]]['E'] = list()
        enfa.transitions[enfa.finals[0]]['E'].append(enfa.initial)

    elif whatistype == 'Or':
        enfa1 = parseENFA(parsed_tree.value[0])
        enfa2 = parseENFA(parsed_tree.value[1])
        newENFA.initial = state_idx
        newENFA.finals.append(state_idx + 1)
        state_idx += 2

        newENFA.states = enfa1.states + enfa2.states
        newENFA.states.append(newENFA.initial)
        newENFA.states.append(newENFA.finals[0])

        newENFA.transitions.update(enfa1.transitions)
        newENFA.transitions.update(enfa2.transitions)

        newENFA.transitions[newENFA.initial] = dict()
        newENFA.transitions[newENFA.initial]['E'] = [enfa1.initial, enfa2.initial]

        if not (enfa1.finals[0] in newENFA.transitions):
            newENFA.transitions[enfa1.finals[0]] = dict()
        if not ('E' in newENFA.transitions[enfa1.finals[0]]):
            newENFA.transitions[enfa1.finals[0]]['E'] = list()
        newENFA.transitions[enfa1.finals[0]]['E'].append(newENFA.finals[0])

        if not (enfa2.finals[0] in newENFA.transitions):
            newENFA.transitions[enfa2.finals[0]] = dict()
        if not ('E' in newENFA.transitions[enfa2.finals[0]]):
            newENFA.transitions[enfa2.finals[0]]['E'] = list()
        newENFA.transitions[enfa2.finals[0]]['E'].append(newENFA.finals[0])

    elif whatistype == 'Epsilon':
        newENFA.initial = state_idx
        newENFA.finals.append(state_idx + 1)
        state_idx += 2

        newENFA.states = [newENFA.initial, newENFA.finals[0]]
        newENFA.transitions[newENFA.initial] = dict()
        newENFA.transitions[newENFA.initial]['E'] = [newENFA.finals[0]]

    return newENFA


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

                closure_idx = list(closure)
                closure_idx.sort()
                closure_idx = tuple(closure_idx)
                if not closure_idx in new_transitions:
                    new_transitions[closure_idx] = dict()
                new_transitions[closure_idx][symbol] = next_closure
                # print (str(closure) + ': ' + symbol + ' -> ' + str(next_closure))

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

def minimizeDFA(DFAset):
    # using hopcraft algorithm
    hop_dict = dict()
    new_hop_dict = {(0): [], (1): []}

    idx = 0
    for state in DFAset.states:
        if state in DFAset.finals:
            new_hop_dict[(1)].append(state)
        else:
            new_hop_dict[(0)].append(state)
    # print ('==============================')
    while hop_dict != new_hop_dict:
        hop_dict = new_hop_dict
        # print (hop_dict)
        new_hop_dict = dict()

        for state in DFAset.states:
            tuple_state = list(state)
            tuple_state.sort()
            tuple_state = tuple(tuple_state)
            idx = 0
            dict_keys = list(hop_dict.keys())
            dict_keys.sort()
            for i in range(len(dict_keys)):
                if state in hop_dict[dict_keys[i]]:
                    idx = i
                    break
            idx_list = [idx]

            for symbol in DFAset.input_symbol:
                if not (tuple_state in DFAset.transitions):
                    idx_list.append(-1)
                elif not (symbol in DFAset.transitions[tuple_state]):
                    idx_list.append(-1)
                else:
                    idx = 0
                    for i in range(len(dict_keys)):
                        if DFAset.transitions[tuple_state][symbol] in hop_dict[dict_keys[i]]:
                            idx = i
                            break
                    idx_list.append(idx)

            idx_tuple = tuple(idx_list)
            if not (idx_tuple in new_hop_dict):
                new_hop_dict[idx_tuple] = list()
            new_hop_dict[idx_tuple].append(state)

    # print ('==============================')
    # print (new_hop_dict)
    # print ('================================')

    mDFAset = Myset()
    dict_keys = list(new_hop_dict.keys())
    dict_keys.sort()
    newdict = dict()
    for i in range(len(dict_keys)):
        mDFAset.states.append('q' + str(i))
        newdict['q' + str(i)] = new_hop_dict[dict_keys[i]]
        if DFAset.initial in new_hop_dict[dict_keys[i]]:
            mDFAset.initial = 'q' + str(i)
        for state in DFAset.finals:
            if state in new_hop_dict[dict_keys[i]]:
                mDFAset.finals.append('q' + str(i))
                break
    # print ('=============================')
    # print (mDFAset.states)
    # print (newdict)

    mDFAset.input_symbol = DFAset.input_symbol
    for state in mDFAset.states:
        sample = list(newdict[state][0])
        sample.sort()
        sample = tuple(sample)
        if not (sample in DFAset.transitions):
            continue
        for symbol in DFAset.input_symbol:
            if not (symbol in DFAset.transitions[sample]):
                continue
            for key in newdict.keys():
                if DFAset.transitions[sample][symbol] in newdict[key]:
                    if not (state in mDFAset.transitions):
                        mDFAset.transitions[state] = dict()
                    mDFAset.transitions[state][symbol] = key

    # print (mDFAset.transitions)
    # print (mDFAset.initial)
    # print (mDFAset.finals)

    return mDFAset

def printResult(mDFAset):
    f = open("resource/m-dfa.txt", "w")
    f.write('State\n')
    f.write(mDFAset.states[0])
    if len(mDFAset.states) > 1:
        for i in range(1, len(mDFAset.states)):
            f.write(',' + mDFAset.states[i])
    f.write('\n')

    f.write('Input symbol\n')
    if len(mDFAset.input_symbol) > 0:
        f.write(mDFAset.input_symbol[0])
    if len(mDFAset.input_symbol) > 1:
        for i in range(1, len(mDFAset.input_symbol)):
            f.write(',' + mDFAset.input_symbol[i])
    f.write('\n')

    f.write('State transition function\n')
    keys = list(mDFAset.transitions.keys())
    keys.sort()
    if len(keys) < 1:
        f.write('\n')
    for key in keys:
        symbols = list(mDFAset.transitions[key].keys())
        symbols.sort()
        for symbol in symbols:
            f.write(key + ',' + symbol + ',' + mDFAset.transitions[key][symbol] + '\n')

    f.write('Initial state\n')
    f.write(mDFAset.initial + '\n')

    f.write ('Final state\n')
    f.write (mDFAset.finals[0])
    if len(mDFAset.finals) > 1:
        for i in range(1, len(mDFAset.finals)):
            f.write (',' + mDFAset.finals[i])
    f.write('\n')
    f.close()

if __name__ == '__main__':
    main()
