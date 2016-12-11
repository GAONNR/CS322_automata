### 1: ㄱ    2: ㄴ    3: ㅏㅓ
### q: ㄹ    w: ㅁ    e: ㅗㅜ
### a: ㅅ    s: ㅇ    d: ㅣ
### z: 획    x: ㅡ    c: 쌍

### moeum_starts_with = '3edx'
### jaeum_starts_with = '12qwas'

jamo_transition = {
    's': {'1': 'ㄱ', '2': 'ㄴ', '3': 'ㅏ',
          'q': 'ㄹ', 'w': 'ㅁ', 'e': 'ㅗ',
          'a': 'ㅅ', 's': 'ㅇ', 'd': 'ㅣ',
          'x': 'ㅡ'},
    'ㄱ': {'z': 'ㅋ', 'c': 'ㄲ'},
    'ㄴ': {'z': 'ㄷ'},
    'ㄷ': {'z': 'ㅌ', 'c': 'ㄸ'},
    'ㅁ': {'z': 'ㅂ'},
    'ㅂ': {'z': 'ㅍ', 'c': 'ㅃ'},
    'ㅅ': {'z': 'ㅈ', 'c': 'ㅆ'},
    'ㅇ': {'z': 'ㅎ'},
    'ㅈ': {'z': 'ㅊ', 'c': 'ㅉ'},
    'ㅏ': {'z': 'ㅑ'},
    'ㅑ': {'z': 'ㅒ'},
    'ㅓ': {'z': 'ㅕ'},
    'ㅗ': {'z': 'ㅛ'},
    'ㅜ': {'z': 'ㅠ'},
}

# ('ㄱ', 'ㅅ'): 'ㄳ', ('ㅂ', 'ㅅ'): 'ㅄ', ('ㄴ', 'ㅈ'): 'ㄵ', ('ㄴ', 'ㅎ'): 'ㄶ', ('ㄹ', 'ㄱ'): 'ㄺ',
# ('ㄹ', 'ㅁ'): 'ㄻ', ('ㄹ', 'ㅂ'): 'ㄼ', ('ㄹ', 'ㅅ'): 'ㄽ', ('ㄹ', 'ㅌ'): 'ㄾ', ('ㄹ', 'ㅍ'): 'ㄿ',
# ('ㄹ', 'ㅎ'): 'ㅀ'

order_cho = {
    'ㄱ': 0, 'ㄲ': 1, 'ㄴ': 2, 'ㄷ': 3, 'ㄸ': 4,
    'ㄹ': 5, 'ㅁ': 6, 'ㅂ': 7, 'ㅃ': 8, 'ㅅ': 9,
    'ㅆ': 10, 'ㅇ': 11, 'ㅈ': 12, 'ㅉ': 13, 'ㅊ': 14,
    'ㅋ': 15, 'ㅌ': 16, 'ㅍ': 17, 'ㅎ': 18
}

order_jung = {
    'ㅏ': 0, 'ㅐ': 1, 'ㅑ': 2, 'ㅒ': 3, 'ㅓ': 4,
    'ㅔ': 5, 'ㅕ': 6, 'ㅖ': 7, 'ㅗ': 8, 'ㅘ': 9,
    'ㅙ': 10, 'ㅚ': 11, 'ㅛ': 12, 'ㅜ': 13, 'ㅝ': 14,
    'ㅞ': 15, 'ㅟ': 16, 'ㅠ': 17, 'ㅡ': 18, 'ㅢ': 19,
    'ㅣ': 20
}

order_jong = {
    None: 0, 'ㄱ': 1, 'ㄲ': 2, 'ㄳ': 3, 'ㄴ': 4,
    'ㄵ': 5, 'ㄶ': 6, 'ㄷ': 7, 'ㄹ': 8, 'ㄺ': 9,
    'ㄻ': 10, 'ㄼ': 11, 'ㄽ': 12, 'ㄾ': 13, 'ㄿ': 14,
    'ㅀ': 15, 'ㅁ': 16, 'ㅂ': 17, 'ㅄ': 18, 'ㅅ': 19,
    'ㅆ': 20, 'ㅇ': 21, 'ㅈ': 22, 'ㅊ': 23, 'ㅋ': 24,
    'ㅌ': 25, 'ㅍ': 26, 'ㅎ': 27
}

class DFA:
    def __init__(self):
        self.states = list()
        self.symbols = list()
        self.transitions = dict()
        self.initial = str()
        self.final = list()

def getDFA(path, dfa):
    fDFA = open(path, "r")
    newReadline = lambda f: f.readline().strip()

    ### read state
    line = newReadline(fDFA)
    dfa.states = newReadline(fDFA).split(',')

    ### read symbol
    line = newReadline(fDFA)
    dfa.symbols = newReadline(fDFA).split(',')

    ### read function
    line = newReadline(fDFA)
    line = newReadline(fDFA)
    while line != 'Initial state' and line:
        currS, sym, nextS = line.split(',')
        if not (currS in dfa.transitions): dfa.transitions[currS] = dict()
        dfa.transitions[currS][sym] = nextS
        line = newReadline(fDFA)

    ### read initial state
    dfa.initial = newReadline(fDFA)

    ### read final state
    line = newReadline(fDFA)
    dfa.final = newReadline(fDFA).split(',')

    fDFA.close()

def match(dfa, mystr):
    currS = dfa.initial
    for al in mystr:
        if not (currS in dfa.transitions): return False
        if not (al in dfa.transitions[currS]): return False

        currS = dfa.transitions[currS][al]

    if currS in dfa.final: return True
    else: return False
