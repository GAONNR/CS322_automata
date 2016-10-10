#-*- coding: utf-8 -*-
import sys

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

SIGKILL = chr(0x04)
SIGSTOP = chr(0x03)
BACKSPACE = chr(0x7f)

keymap = {'q': u'ㅂ', 'w': u'ㅈ', 'e': u'ㄷ', 'r': u'ㄱ', 't': u'ㅅ',
          'y': u'ㅛ', 'u': u'ㅕ', 'i': u'ㅑ', 'o': u'ㅐ', 'p': u'ㅔ',
          'a': u'ㅁ', 's': u'ㄴ', 'd': u'ㅇ', 'f': u'ㄹ', 'g': u'ㅎ',
          'h': u'ㅗ', 'j': u'ㅓ', 'k': u'ㅏ', 'l': u'ㅣ', 'z': u'ㅋ',
          'x': u'ㅌ', 'c': u'ㅊ', 'v': u'ㅍ', 'b': u'ㅠ', 'n': u'ㅜ',
          'm': u'ㅡ', 'Q': u'ㅃ', 'W': u'ㅉ', 'E': u'ㄸ', 'R': u'ㄲ',
          'T': u'ㅆ', 'O': u'ㅒ', 'P': u'ㅖ'}

def unicodePrinter(key):
    if not key in keymap:
        print key,
    else:
        print keymap[key],

def batchimFirst():
    chara = getch()
    while chara != SIGKILL and chara != SIGSTOP:
        unicodePrinter(chara)
        chara = getch()

def choseongFirst():
    chara = getch()
    while chara != SIGKILL and chara != SIGSTOP:
        unicodePrinter(chara)
        chara = getch()

if __name__ == '__main__':
    print u'한글 모아쓰기 표시 방법을 선택하세요.'
    way_of_writing = int(raw_input("받침우선: 0, 초성우선: 1    $ "))

    if way_of_writing == 0:
        batchimFirst()
    elif way_of_writing == 1:
        choseongFirst()
    else:
        print 'Invalid Input'
        sys.exit(1)

    print u'\n잘가영'
