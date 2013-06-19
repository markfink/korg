import sys
import regex
import glob
import os


def load_pattern_file(filename, pm):
    pattern_re = regex.compile("^(?P<patname>\w+) (?P<pattern>.+)$")
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        m = pattern_re.search(line)
        if m:
            md = m.groupdict()
            pm[md['patname']] = md['pattern']


def load_patterns(folders):
    """Load all pattern from all the files in folders"""
    pm = {}
    for folder in folders:
        for file in os.listdir(folder):
            if regex.match(r'^[\w-]+$', file):
                load_pattern_file(os.path.join(folder, file), pm)
    return pm


if __name__ == '__main__':
    print load_patterns(['../patterns'])