import sys
import regex  # compared to re this implements the full regex spec like atomic grouping
from pattern import PatternRepo

class LineGrokker(object):
    # TODO: can't say if this is a useful interface. Please provide feedback on any thoughts.
    def __init__(self, pattern, pattern_repo):
        self.regex = pattern_repo.compile_regex(pattern)

    def grok(self, data):
        m = self.regex.search(data)
        if m:
            return m.groupdict()


if __name__ == "__main__":
    GLOBALPM = {
        'HOST': '[\w+\._-]+',
        'PORT': '\d+',
        'PROG': '\w+',
        'USER': '\w+',
    }
    pr = PatternRepo([], False, GLOBALPM)
    g = LineGrokker('%{HOST} %{PROG:progi}\[\d+\]: error: PAM: authentication error for %{USER} from %{HOST:SRC}', pr)

    print g.grok('HOST PROG[1234]: error: PAM: authentication error for USER from SRC')
