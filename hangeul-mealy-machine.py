#-*- coding: utf-8 -*-
import sys
import string

### Code lines below this comment is to implement getting a keyboard event.
### Reference: http://code.activestate.com/recipes/134892/

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

### End of the reference code

reload(sys)
sys.setdefaultencoding('utf-8')
getch = _Getch()
## clearScr = _clearScreen()

SIGEXIT = [chr(0x04), chr(0x03), chr(0x0d)]
BACKSPACE = chr(0x7f)

keymap = {'q': u'ㅂ', 'w': u'ㅈ', 'e': u'ㄷ', 'r': u'ㄱ', 't': u'ㅅ',
          'y': u'ㅛ', 'u': u'ㅕ', 'i': u'ㅑ', 'o': u'ㅐ', 'p': u'ㅔ',
          'a': u'ㅁ', 's': u'ㄴ', 'd': u'ㅇ', 'f': u'ㄹ', 'g': u'ㅎ',
          'h': u'ㅗ', 'j': u'ㅓ', 'k': u'ㅏ', 'l': u'ㅣ', 'z': u'ㅋ',
          'x': u'ㅌ', 'c': u'ㅊ', 'v': u'ㅍ', 'b': u'ㅠ', 'n': u'ㅜ',
          'm': u'ㅡ', 'Q': u'ㅃ', 'W': u'ㅉ', 'E': u'ㄸ', 'R': u'ㄲ',
          'T': u'ㅆ', 'O': u'ㅒ', 'P': u'ㅖ'}
choseong = {u'ㄱ': 0, u'ㄲ': 1, u'ㄴ': 2, u'ㄷ': 3, u'ㄸ': 4,
            u'ㄹ': 5, u'ㅁ': 6, u'ㅂ': 7, u'ㅃ': 8, u'ㅅ': 9,
            u'ㅆ': 10, u'ㅇ': 11, u'ㅈ': 12, u'ㅉ': 13, u'ㅊ': 14,
            u'ㅋ': 15, u'ㅌ': 16, u'ㅍ': 17, u'ㅎ': 18}
jungseong = {u'ㅏ': 0, u'ㅐ': 1, u'ㅑ': 2, u'ㅒ': 3, u'ㅓ': 4,
             u'ㅔ': 5, u'ㅕ': 6, u'ㅖ': 7, u'ㅗ': 8, u'ㅘ': 9,
             u'ㅙ': 10, u'ㅚ': 11, u'ㅛ': 12, u'ㅜ': 13, u'ㅝ': 14,
             u'ㅞ': 15, u'ㅟ': 16, u'ㅠ': 17, u'ㅡ': 18, u'ㅢ': 19,
             u'ㅣ': 20}
jongseong = {None: 0, u'ㄱ': 1, u'ㄲ': 2, u'ㄳ': 3, u'ㄴ': 4,
             u'ㄵ': 5, u'ㄶ': 6, u'ㄷ': 7, u'ㄹ': 8, u'ㄺ': 9,
             u'ㄻ': 10, u'ㄼ': 11, u'ㄽ': 12, u'ㄾ': 13, u'ㄿ': 14,
             u'ㅀ': 15, u'ㅁ': 16, u'ㅂ': 17, u'ㅄ': 18, u'ㅅ': 19,
             u'ㅆ': 20, u'ㅇ': 21, u'ㅈ': 22, u'ㅊ': 23, u'ㅋ': 24,
             u'ㅌ': 25, u'ㅍ': 26, u'ㅎ': 27}

gyeopbatchim = {u'ㄳ': [u'ㄱ', u'ㅅ'], u'ㄵ': [u'ㄴ', u'ㅈ'], u'ㄶ': [u'ㄴ', u'ㅎ'], u'ㄺ': [u'ㄹ', u'ㄱ'],
               u'ㄻ': [u'ㄹ', u'ㅁ'], u'ㄼ': [u'ㄹ', u'ㅂ'], u'ㄽ': [u'ㄹ', u'ㅅ'], u'ㄾ': [u'ㄹ', u'ㅌ'],
               u'ㄿ': [u'ㄹ', u'ㅍ'], u'ㅀ': [u'ㄹ', u'ㅎ'], u'ㅄ': [u'ㅂ', u'ㅅ']}
gyeopmoeum = {u'ㅘ': u'ㅗ', u'ㅙ': u'ㅗ', u'ㅚ': u'ㅗ', u'ㅝ': u'ㅜ', u'ㅞ': u'ㅜ', u'ㅟ': u'ㅜ', u'ㅢ': u'ㅡ'}

jaeum2gyeop = {(u'ㄱ', u'ㅅ'): u'ㄳ', (u'ㅂ', u'ㅅ'): u'ㅄ', (u'ㄴ', u'ㅈ'): u'ㄵ', (u'ㄴ', u'ㅎ'): u'ㄶ', (u'ㄹ', u'ㄱ'): u'ㄺ',
               (u'ㄹ', u'ㅁ'): u'ㄻ', (u'ㄹ', u'ㅂ'): u'ㄼ', (u'ㄹ', u'ㅅ'): u'ㄽ', (u'ㄹ', u'ㅌ'): u'ㄾ', (u'ㄹ', u'ㅍ'): u'ㄿ',
               (u'ㄹ', u'ㅎ'): u'ㅀ'}

class State:
    def __init__(self, state):
        self.state = state # initial State
        self.chara_list = []
        self.completed = False

    def append(self, chara):
        self.chara_list.append(chara)

    def pop(self):
        return self.chara_list.pop()

    def len(self):
        return len(self.chara_list)

    def get(self, idx):
        return self.chara_list[idx]

    def __str__(self):
        return "[state: " + self.state + ", " + str(self.chara_list) + "]"

state_list = []

def batchimFirst(chara, state):
    if state.state == 'S':
        if chara in choseong:
            state.append(chara)
            state.state = 'V'
        else:
            state.state = 'V'
            return batchimFirst(chara, state)
        return state

    elif state.state == 'V':
        if not chara in jungseong:
            state.completed = True
            new_state = State('V')
            new_state.append(chara)
            state_list.append(new_state)
            return new_state
        else:
            if chara == u'ㅗ':
                state.state = 'O'
            elif chara == u'ㅜ':
                state.state = 'U'
            elif chara in [u'ㅏ', u'ㅑ', u'ㅓ', u'ㅕ', u'ㅡ']:
                state.state = 'A'
            elif chara in [u'ㅛ', u'ㅠ', u'ㅣ', u'ㅐ', u'ㅔ', u'ㅒ', u'ㅖ']:
                state.state = 'I'
            state.append(chara)
            return state

    elif state.state in ['O', 'U', 'A', 'I']:
        if not chara in jongseong:
            last_chara = state.pop()
            if state.state == 'O' and chara == 'ㅏ':
                state.state = 'A'
                state.append(u'ㅘ')
            elif state.state == 'O' and chara == 'ㅣ':
                state.state = 'I'
                state.append(u'ㅚ')
            elif state.state == 'O' and chara == 'ㅐ':
                state.state = 'I'
                state.append(u'ㅙ')
            elif state.state == 'U' and chara == 'ㅓ':
                state.state = 'A'
                state.append(u'ㅝ')
            elif state.state == 'U' and chara == 'ㅣ':
                state.state = 'I'
                state.append(u'ㅟ')
            elif state.state == 'U' and chara == 'ㅔ':
                state.state == 'I'
                state.append(u'ㅞ')
            elif last_chara == 'ㅡ' and chara == 'ㅣ':
                state.state = 'I'
                state.append(u'ㅢ')
            else:
                state.completed = True
                state.append(last_chara)
                new_state = batchimFirst(chara, State('S'))
                state_list.append(new_state)
                return new_state
            return state

        else:
            if chara in [u'ㄱ', u'ㅂ']:
                state.state = 'K'
            elif chara == u'ㄴ':
                state.state = 'N'
            elif chara == u'ㄹ':
                state.state = 'R'
            elif chara in [u'ㄷ', u'ㅁ', u'ㅅ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ', u'ㄲ', u'ㅆ']:
                state.state = 'L'
            if not state.get(0) in jungseong:
                state.append(chara)
                return state
            else:
                state.completed = True
                new_state = State('S')
                state_list.append(new_state)
                return batchimFirst(chara, new_state)

    elif state.state in ['K', 'N', 'R', 'L']:
        if not chara in choseong:
            last_chara = state.pop()
            if last_chara in gyeopbatchim:
                state.append(gyeopbatchim[last_chara][0])
                last_chara = gyeopbatchim[last_chara][1]
            state.completed = True
            new_state = State('V')
            new_state.append(last_chara)
            state_list.append(new_state)
            return batchimFirst(chara, new_state)
        else:
            last_chara = state.pop()
            if (last_chara, chara) in jaeum2gyeop:
                state.state = 'L'
                state.append(jaeum2gyeop[(last_chara, chara)])
            else:
                state.completed = True
                state.append(last_chara)
                new_state = State('S')
                state_list.append(new_state)
                return batchimFirst(chara, new_state)
            ### new_state = State('S')
            ### state_list.append(new_state)
            return state

    else:
        return state

def choseongFirst(chara, state):
    if len(state_list) > 2:
        state_list[-3].completed = True
    if state.state == 'S':
        ### 모음 먼저는 나중에
        if chara in choseong:
            state.append(chara)
            state.state = 'V'
        else:
            state.state = 'V'
            return choseongFirst(chara, state)
        return state

    elif state.state == 'V':
        if not chara in jungseong:
            state_list.pop()
            past_state = state_list[-1]
            if past_state.state in ['K', 'N', 'R', 'L']:
                last_chara = past_state.pop()
                state_chara = state.pop()
                if (last_chara, state_chara) in jaeum2gyeop:
                    past_state.state = 'L'
                    past_state.append(jaeum2gyeop[(last_chara, state_chara)])
                    past_state.completed = True
                    new_state = State('S')
                    state_list.append(new_state)
                    return choseongFirst(chara, new_state)
                else:
                    past_state.append(last_chara)
                    new_state = State('S')
                    past_state.completed = True
                    state_list.append(new_state)
                    new_state.completed = True
                    choseongFirst(state_chara, new_state)
                    new_new_state = State('S')
                    state_list.append(new_new_state)
                    return choseongFirst(chara, new_new_state)
            elif past_state.state in ['O', 'U', 'A', 'I']:
                state_chara = state.pop()
                if state_chara in [u'ㄱ', u'ㅂ']:
                    past_state.state = 'K'
                elif state_chara == u'ㄴ':
                    past_state.state = 'N'
                elif state_chara == u'ㄹ':
                    past_state.state = 'R'
                elif state_chara in [u'ㄷ', u'ㅁ', u'ㅅ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ', u'ㄲ', u'ㅆ']:
                    past_state.state = 'L'
                past_state.append(state_chara)
                state.append(chara)
                state_list.append(state)
                return state
            else:
                state_list.append(state)
                state.completed = True
                new_state = State('S')
                state_list.append(new_state)
                return choseongFirst(chara, new_state)
        else:
            if chara == u'ㅗ':
                state.state = 'O'
            elif chara == u'ㅜ':
                state.state = 'U'
            elif chara in [u'ㅏ', u'ㅑ', u'ㅓ', u'ㅕ', u'ㅡ']:
                state.state = 'A'
            elif chara in [u'ㅛ', u'ㅠ', u'ㅣ', u'ㅐ', u'ㅔ', u'ㅒ', u'ㅖ']:
                state.state = 'I'
            state.append(chara)
            if len(state_list) > 3:
                state_list[-2].completed = True
            return state

    elif state.state in ['O', 'U', 'A', 'I']:
        if not chara in jongseong:
            last_chara = state.pop()
            if state.state == 'O' and chara == 'ㅏ':
                state.state = 'A'
                state.append(u'ㅘ')
            elif state.state == 'O' and chara == 'ㅣ':
                state.state = 'I'
                state.append(u'ㅚ')
            elif state.state == 'O' and chara == 'ㅐ':
                state.state = 'I'
                state.append(u'ㅙ')
            elif state.state == 'U' and chara == 'ㅓ':
                state.state = 'A'
                state.append(u'ㅝ')
            elif state.state == 'U' and chara == 'ㅣ':
                state.state = 'I'
                state.append(u'ㅟ')
            elif state.state == 'U' and chara == 'ㅔ':
                state.state == 'I'
                state.append(u'ㅞ')
            elif last_chara == 'ㅡ' and chara == 'ㅣ':
                state.state = 'I'
                state.append(u'ㅢ')
            else:
                state.append(last_chara)
                state.completed = True
                new_state = batchimFirst(chara, State('S'))
                state_list.append(new_state)
                return new_state
            return state

        else:
            new_state = State('S')
            state_list.append(new_state)
            return batchimFirst(chara, new_state)

    elif state.state in ['K', 'N', 'R', 'L']:
        new_state = State('S')
        state_list.append(new_state)
        return choseongFirst(chara, new_state)

    else:
        return state

def printer(state):
    if state.len() == 1:
        sys.stdout.write(state.get(0))
    elif state.len() == 2:
        if state.get(0) in choseong:
            cho = choseong[state.get(0)]
            jung = jungseong[state.get(1)]

            result = unichr(0xAC00 + 28 * 21 * cho + 28 * jung)
            sys.stdout.write(result)
        else:
            sys.stdout.write(state.get(0))
    elif state.len() == 3:
        cho = choseong[state.get(0)]
        jung = jungseong[state.get(1)]
        jong = jongseong[state.get(2)]

        result = unichr(0xAc00 + 28 * 21 * cho + 28 * jung + jong)
        sys.stdout.write(result)
    else:
        return

def typeWriter(way_of_writing):
    if way_of_writing == 0:
        typeFunction = batchimFirst
    elif way_of_writing == 1:
        typeFunction = choseongFirst
    else:
        print 'Invalid Input'
        sys.exit(1)

    curr_state = State('S')
    state_list.append(curr_state)

    while True:
        chara = getch()
        if chara in SIGEXIT:
            return
        elif ord(chara) >= ord('a') and ord(chara) <= ord('z') or (chara in 'QWERTOP'):
            chara = keymap[chara]
            curr_state = typeFunction(chara, curr_state)
        elif chara in string.printable:
            curr_state.completed = True
            new_state = State('S')
            new_state.append(chara)
            state_list.append(new_state)
            new_state.completed = True
            curr_state = State('S')
            state_list.append(curr_state)
        elif ord(chara) == 0x7f:
            ### delete
            if curr_state.completed:
                state_list.pop()
                if not state_list:
                    state_list.append(State('S'))
                curr_state = state_list[-1]
            else:
                try:
                    last = curr_state.pop()
                    if last in gyeopbatchim:
                        curr_state.append(gyeopbatchim[last][0])
                    elif last in gyeopmoeum:
                        curr_state.append(gyeopmoeum[last])
                    if curr_state.len() == 0:
                        state_list.pop()
                        if not state_list:
                            state_list.append(State('S'))
                        curr_state = state_list[-1]
                except:
                    state_list.pop()
                    if not state_list:
                        state_list.append(State('S'))
                    state_list.pop()
                    if not state_list:
                        state_list.append(State('S'))
                    curr_state = state_list[-1]
        else:
            continue
        sys.stdout.write('\x1b[2K\r')
        for state in state_list:
            printer(state)

if __name__ == '__main__':
    print u'한글 모아쓰기 표시 방법을 선택하세요.'
    way_of_writing = int(raw_input("받침우선: 0, 초성우선: 1    $ "))

    ## clearScr()
    typeWriter(way_of_writing)
    print u'\nGood Bye'
