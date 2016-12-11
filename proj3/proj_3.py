# ((1+1c+2+2z+2zc+q+w+wz+wzc+a+ac+s+az+azc+azz+1z+2zz+wzz+sz)
# (3+3d+3z+3zd+33+33d+33z+33zd+e+e3+e3d+ed+ez+ee+ee3+ee3d+eed+eez+x+xd+d)
# (()+1+1c+1a+2+2az+2sz+2z+q+q1+qw+qa+q2zz+qwzz+qsz+w+wz+wza+a+ac+s+az+azz+1z+2zz+wzz+sz))*

# keyregex = '((1+1c+2+2z+2zc+q+w+wz+wzc+a+ac+s+az+azc+azz+1z+2zz+wzz+sz)(3+3d+3z+3zd+33+33d+33z+33zd+e+e3+e3d+ed+ez+ee+ee3+ee3d+eed+eez+x+xd+d)(()+1+1c+1a+2+2az+2sz+2z+q+q1+qw+qa+q2zz+qwzz+qsz+w+wz+wza+a+ac+s+az+azz+1z+2zz+wzz+sz))*'

import sys, accepter
from accepter import DFA, jamo_transition
from accepter import order_cho, order_jung, order_jong

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty

    def __call__(self):
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

hangeul_transitions = dict()
keyset = [0x31, 0x32, 0x33, 0x71, 0x77, 0x65, 0x61, 0x73, 0x64, 0x7a, 0x78, 0x63, 0x7f]
chos = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
jungs = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
jongs = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
gyeopjs = 'ㄳㄵㄶㄺㄻㄼㄽㄾㄿㅀ'

jaeum_gyeop = {('ㄱ', 'ㅅ'): 'ㄳ', ('ㅂ', 'ㅅ'): 'ㅄ', ('ㄴ', 'ㅈ'): 'ㄵ', ('ㄴ', 'ㅎ'): 'ㄶ', ('ㄹ', 'ㄱ'): 'ㄺ',
               ('ㄹ', 'ㅁ'): 'ㄻ', ('ㄹ', 'ㅂ'): 'ㄼ', ('ㄹ', 'ㅅ'): 'ㄽ', ('ㄹ', 'ㅌ'): 'ㄾ', ('ㄹ', 'ㅍ'): 'ㄿ',
               ('ㄹ', 'ㅎ'): 'ㅀ'}
moeum_gyeop = {('ㅏ', 'ㅣ'): 'ㅐ', ('ㅓ', 'ㅣ'): 'ㅔ', ('ㅑ', 'ㅣ'): 'ㅒ', ('ㅕ', 'ㅣ'): 'ㅖ',
               ('ㅜ', 'ㅏ'): 'ㅝ', ('ㅜ', 'ㅓ'): 'ㅝ', ('ㅝ', 'ㅣ'): 'ㅞ', ('ㅗ', 'ㅏ'): 'ㅘ', ('ㅘ', 'ㅣ'): 'ㅙ', ('ㅗ', 'ㅣ'): 'ㅚ',
               ('ㅜ', 'ㅣ'): 'ㅟ', ('ㅡ', 'ㅣ'): 'ㅢ'}
gyeop_jaeum = {'ㄳ': ['ㄱ', 'ㅅ'], 'ㄵ': ['ㄴ', 'ㅈ'], 'ㄶ': ['ㄴ', 'ㅎ'], 'ㄺ': ['ㄹ', 'ㄱ'],
               'ㄻ': ['ㄹ', 'ㅁ'], 'ㄼ': ['ㄹ', 'ㅂ'], 'ㄽ': ['ㄹ', 'ㅅ'], 'ㄾ': ['ㄹ', 'ㅌ'],
               'ㄿ': ['ㄹ', 'ㅍ'], 'ㅀ': ['ㄹ', 'ㅎ'], 'ㅄ': ['ㅂ', 'ㅅ']}


getch = _Getch()

class JAMO:
    def __init__(self, s, is_jaeum):
        self.s = s
        self.is_jaeum = is_jaeum
    def __str__(self):
        if self.is_jaeum: return '%s' % self.s
        else: return '%s' % self.s

class GEULJA:
    def __init__(self):
        self.cho    = None
        self.jung   = None
        self.jong   = None
    def __str__(self):
        if not self.cho: return ''
        if not self.jung: return self.cho
        return chr(0xac00 + 28 * 21 * order_cho[self.cho] + 28 * order_jung[self.jung] + order_jong[self.jong])

def rawParser(dfa, stack, v):
    if not stack: return
    str_stack = ''.join(stack)
    if not (accepter.match(dfa, str_stack)) and v: return

    moeum_starts_with = '3edx'
    jaeum_starts_with = '12qwas'
    sp_stack = list()
    si = 0
    for i in range(1, len(stack)):
        if stack[i] in jaeum_starts_with:
            sp_stack.append(stack[si : i])
            si = i
        elif stack[i] in moeum_starts_with:
            sp_stack.append(stack[si : i])
            si = i

    if stack[si] in jaeum_starts_with: sp_stack.append(stack[si : len(stack)])
    elif stack[si] in moeum_starts_with: sp_stack.append(stack[si : len(stack)])
    return sp_stack

def jamoParser(stack):
    if not stack: return None
    jamo_stack = list()
    moeum_starts_with = '3edx'

    for el in stack:
        s, is_jaeum = 's', True
        if el[0] in moeum_starts_with: is_jaeum = False
        for sym in el:
            if not (sym in jamo_transition[s]): continue
            s = jamo_transition[s][sym]
        jamo_stack.append(JAMO(s, is_jaeum))

    return jamo_stack

def jamoMerger(stack):
    jamo_stack, idx = list(), 0
    while idx < len(stack):
        if stack[idx].is_jaeum: jamo_stack.append(stack[idx])
        elif idx + 1 == len(stack): jamo_stack.append(stack[idx])
        else:
            if stack[idx].s == stack[idx + 1].s:
                if stack[idx].s == 'ㅏ':
                    jamo_stack.append(JAMO('ㅓ', False))
                    idx += 1
                elif stack[idx].s == 'ㅗ':
                    jamo_stack.append(JAMO('ㅜ', False))
                    idx += 1
                else:
                    jamo_stack.append(stack[idx])
            elif stack[idx].s == 'ㅏ' and stack[idx + 1].s == 'ㅑ':
                jamo_stack.append(JAMO('ㅕ', False))
                idx += 1
            elif stack[idx].s == 'ㅗ' and stack[idx + 1].s == 'ㅛ':
                jamo_stack.append(JAMO('ㅠ', False))
                idx += 1
            else: jamo_stack.append(stack[idx])
        idx += 1

    return jamo_stack

def geuljaParser(stack, parseFunc):
    geulja_stack, s = [GEULJA()], 's'
    for jamo in stack:
        l = len(geulja_stack)
        # print('%s, %s' % (s, jamo.s), end = ', ')
        s, res = parseFunc(geulja_stack[l - 1], s, jamo)
        if not res: continue
        geulja_stack.append(res)

    return geulja_stack

def choFirst(geulja, s, jamo):
    e = hangeul_transitions[s][jamo.s]
    new_geulja = None
    if   s == 's': geulja.cho = jamo.s
    elif s == 'v': geulja.jung = jamo.s
    elif s == 'o':
        if   e in 'knrl': geulja.jong = jamo.s
        elif e in 'ai':   geulja.jung = moeum_gyeop[(geulja.jung, jamo.s)]
        else:
            new_geulja = GEULJA()
            new_geulja.cho = jamo.s
    elif s == 'u':
        if   e in 'knrl': geulja.jong = jamo.s
        elif e in 'ai': geulja.jung = moeum_gyeop[(geulja.jung, jamo.s)]
        else:
            new_geulja = GEULJA()
            new_geulja.cho = jamo.s
    elif s == 'a':
        if   e in 'knrl': geulja.jong = jamo.s
        elif e in 'i':   geulja.jung = moeum_gyeop[(geulja.jung, jamo.s)]
        else:
            new_geulja = GEULJA()
            new_geulja.cho = jamo.s
    elif s == 'i':
        if   e in 'knrl': geulja.jong = jamo.s
        else:
            new_geulja = GEULJA()
            new_geulja.cho = jamo.s
    elif s in 'knrl':
        if   e in 'ouai':
            new_geulja = GEULJA()
            if geulja.jong in gyeopjs:
                new_geulja.cho = gyeop_jaeum[geulja.jong][1]
                geulja.jong = gyeop_jaeum[geulja.jong][0]
            else:
                new_geulja.cho = geulja.jong
                geulja.jong = None
            new_geulja.jung = jamo.s

        elif e == 'l':    geulja.jong = jaeum_gyeop[(geulja.jong, jamo.s)]
        else:
            new_geulja = GEULJA()
            new_geulja.cho = jamo.s
    # print(s, e)
    return e, new_geulja

def deleter(stack):
    if len(stack) < 1: return stack
    res1 = stack.pop()
    if len(stack) < 1: return stack
    res2 = stack.pop()

    if res1 == 'z': return stack
    if (res1 == '3') and (res1 == res2): return stack
    if (res1 == 'e') and (res1 == res2): return stack
    stack.append(res2)
    return stack

def main():
    mdfa_path = 'proj3_mdfa.txt'
    dfa, stack = DFA(), list()
    accepter.getDFA(mdfa_path, dfa)
    parsingWay = choFirst
    makeHangeulTransition()
    # print(hangeul_transitions)

    while True:
        c = getch().lower()
        if not (ord(c) in keyset):
            print('\nByeBye')
            break

        if ord(c) == 0x7f: stack = deleter(stack)
        else: stack.append(c)

        idx, sp_stack = len(stack), rawParser(dfa, stack, True)
        while not sp_stack:
            sp_stack = rawParser(dfa, stack[:idx], True)
            idx = idx - 1
            if idx <= 0: break

        sys.stdout.write('\x1b[2K\r')
        if idx > 0:
            jamo_stack = jamoParser(sp_stack)
            jamo_stack = jamoMerger(jamo_stack)
            # sys.stdout.write('\n')
            # for jamo in jamo_stack: print(jamo, end = '')
            # sys.stdout.write('\n')

            geulja_stack = geuljaParser(jamo_stack, parsingWay)
            for geulja in geulja_stack: print(geulja, end = '')
        if idx <= 0: idx = -1
        if stack[idx + 1:] != []:
            # print('\n' + str(idx) + ': ' + str(stack[idx + 1:]))
            sp_stack = rawParser(dfa, stack[idx + 1:], False)
            if not (not sp_stack):
                jamo_stack = jamoParser(sp_stack)
                for jamo in jamo_stack: print(jamo, end = '')
        sys.stdout.flush()
    return

def makeHangeulTransition():
    hangeul_transitions['s'] = dict()
    append2Dict(hangeul_transitions, 's', chos, 'v')

    hangeul_transitions['v'] = dict()
    hangeul_transitions['v']['ㅗ'] = 'o'
    hangeul_transitions['v']['ㅜ'] = 'u'
    append2Dict(hangeul_transitions, 'v', 'ㅏㅑㅓㅕㅡ', 'a')
    append2Dict(hangeul_transitions, 'v', 'ㅛㅠㅣ', 'i')

    hangeul_transitions['o'] = dict()
    append2Dict(hangeul_transitions, 'o', 'ㄱㅂ', 'k')
    hangeul_transitions['o']['ㄴ'] = 'n'
    hangeul_transitions['o']['ㄹ'] = 'r'
    append2Dict(hangeul_transitions, 'o', 'ㄷㅁㅅㅇㅈㅊㅋㅌㅍㅎㄲㅆ', 'k')
    hangeul_transitions['o']['ㅏ'] = 'a'
    hangeul_transitions['o']['ㅣ'] = 'i'
    append2Dict(hangeul_transitions, 'o', 'ㄸㅃㅉ', 'v')

    hangeul_transitions['u'] = dict()
    append2Dict(hangeul_transitions, 'u', 'ㄱㅂ', 'k')
    hangeul_transitions['u']['ㄴ'] = 'n'
    hangeul_transitions['u']['ㄹ'] = 'r'
    append2Dict(hangeul_transitions, 'u', 'ㄷㅁㅅㅇㅈㅊㅋㅌㅍㅎㄲㅆ', 'k')
    hangeul_transitions['u']['ㅏ'] = 'a'
    hangeul_transitions['u']['ㅓ'] = 'a'
    hangeul_transitions['u']['ㅣ'] = 'i'
    append2Dict(hangeul_transitions, 'u', 'ㄸㅃㅉ', 'v')

    hangeul_transitions['a'] = dict()
    append2Dict(hangeul_transitions, 'a', 'ㄱㅂ', 'k')
    hangeul_transitions['a']['ㄴ'] = 'n'
    hangeul_transitions['a']['ㄹ'] = 'r'
    append2Dict(hangeul_transitions, 'a', 'ㄷㅁㅅㅇㅈㅊㅋㅌㅍㅎㄲㅆ', 'k')
    hangeul_transitions['a']['ㅣ'] = 'i'
    append2Dict(hangeul_transitions, 'a', 'ㄸㅃㅉ', 'v')

    hangeul_transitions['i'] = dict()
    append2Dict(hangeul_transitions, 'i', 'ㄱㅂ', 'k')
    hangeul_transitions['i']['ㄴ'] = 'n'
    hangeul_transitions['i']['ㄹ'] = 'r'
    append2Dict(hangeul_transitions, 'i', 'ㄷㅁㅅㅇㅈㅊㅋㅌㅍㅎㄲㅆ', 'k')
    append2Dict(hangeul_transitions, 'i', 'ㄸㅃㅉ', 'v')

    hangeul_transitions['k'] = dict()
    hangeul_transitions['k']['ㅗ'] = 'o'
    hangeul_transitions['k']['ㅜ'] = 'u'
    append2Dict(hangeul_transitions, 'k', 'ㅏㅑㅓㅕㅡ', 'a')
    append2Dict(hangeul_transitions, 'k', 'ㅛㅠㅣ', 'i')
    append2Dict(hangeul_transitions, 'k', chos, 'v')
    hangeul_transitions['k']['ㅅ'] = 'l'

    hangeul_transitions['n'] = dict()
    hangeul_transitions['n']['ㅗ'] = 'o'
    hangeul_transitions['n']['ㅜ'] = 'u'
    append2Dict(hangeul_transitions, 'n', 'ㅏㅑㅓㅕㅡ', 'a')
    append2Dict(hangeul_transitions, 'n', 'ㅛㅠㅣ', 'i')
    append2Dict(hangeul_transitions, 'n', chos, 'v')
    append2Dict(hangeul_transitions, 'n', 'ㅈㅎ', 'l')

    hangeul_transitions['r'] = dict()
    hangeul_transitions['r']['ㅗ'] = 'o'
    hangeul_transitions['r']['ㅜ'] = 'u'
    append2Dict(hangeul_transitions, 'r', 'ㅏㅑㅓㅕㅡ', 'a')
    append2Dict(hangeul_transitions, 'r', 'ㅛㅠㅣ', 'i')
    append2Dict(hangeul_transitions, 'r', chos, 'v')
    append2Dict(hangeul_transitions, 'r', 'ㄱㅁㅂㅅㅌㅍㅎ', 'l')

    hangeul_transitions['l'] = dict()
    hangeul_transitions['l']['ㅗ'] = 'o'
    hangeul_transitions['l']['ㅜ'] = 'u'
    append2Dict(hangeul_transitions, 'l', 'ㅏㅑㅓㅕㅡ', 'a')
    append2Dict(hangeul_transitions, 'l', 'ㅛㅠㅣ', 'i')
    append2Dict(hangeul_transitions, 'l', chos, 'v')

def append2Dict(mydict, fr, str, t):
    for s in str: mydict[fr][s] = t

if __name__ == '__main__':
    main()
