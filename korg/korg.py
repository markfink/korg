import sys
import regex  # compared to re this implements the full regex spec like atomic grouping


class LineGrokker(object):
    def __init__(self, pattern, pattern_map):
        self.regex = self.generate_regex(pattern, pattern_map)

    def grok(self, data):
        m = self.regex.search(data)
        if m:
            return m.groupdict()

    def generate_regex(self, pattern, pattern_map):
        """Compile regex from pattern and pattern_map"""
        pattern_re = regex.compile("(?P<substr>%\{(?P<fullname>(?P<patname>\w+)(?::(?P<subname>\w+))?)\})")
        while 1:
            matches = [md.groupdict() for md in pattern_re.finditer(pattern)]
            if len(matches) == 0:
                break
            for md in matches:
                if pattern_map.has_key(md['patname']):
                    if md['subname']:
                        repl = '(?P<%s>%s)' % (md['subname'], pattern_map[md['patname']])
                    else:
                        repl = pattern_map[md['patname']]
                    # print "Replacing %s with %s"  %(md['substr'], repl)
                    pattern = pattern.replace(md['substr'],repl)

        return regex.compile(pattern)


if __name__ == "__main__":
    GLOBALPM = {
        'HOST': '[\w+\._-]+',
        'PORT': '\d+',
        'PROG': '\w+',
        'USER': '\w+',
    }
    g = LineGrokker('%{HOST} %{PROG:progi}\[\d+\]: error: PAM: authentication error for %{USER} from %{HOST:SRC}', GLOBALPM)

    print g.grok('HOST PROG[1234]: error: PAM: authentication error for USER from SRC')
