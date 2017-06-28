# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
# compared to re this implements the full regex spec like atomic grouping
import regex
import os
import codecs

from . import here


class PatternRepo(object):
    def __init__(self, folders=None, import_korg_patterns=True,
                 pattern_dict=None, patterns=None):
        if not folders:
            folders = []
        self.pattern_dict = {}
        if pattern_dict:
            self.pattern_dict = pattern_dict
        if import_korg_patterns:
            folders.append(here('./patterns'))
        self._load_patterns(folders, self.pattern_dict)
        if patterns:
            d = '\n'
            self._load_pattern_lines([e+d for e in patterns.split(d) if e],
                                     self.pattern_dict)

    def compile_regex(self, pattern, flags=0):
        """Compile regex from pattern and pattern_dict"""
        pattern_re = regex.compile('(?P<substr>%\{(?P<fullname>(?P<patname>\w+)(?::(?P<subname>\w+))?)\})')
        while 1:
            matches = [md.groupdict() for md in pattern_re.finditer(pattern)]
            if len(matches) == 0:
                break
            for md in matches:
                if md['patname'] in self.pattern_dict:
                    if md['subname']:
                        # TODO error if more than one occurance
                        if '(?P<' in self.pattern_dict[md['patname']]:
                            # this is not part of the original logstash implementation 
                            # but it might be useful to be able to replace the
                            # group name used in the pattern
                            repl = regex.sub('\(\?P<(\w+)>', '(?P<%s>' % md['subname'],
                                self.pattern_dict[md['patname']], 1)
                        else:
                            repl = '(?P<%s>%s)' % (md['subname'], 
                                self.pattern_dict[md['patname']])
                    else:
                        repl = self.pattern_dict[md['patname']]
                    # print "Replacing %s with %s"  %(md['substr'], repl)
                    pattern = pattern.replace(md['substr'], repl)
                else:
                    # print('patname not found')
                    # maybe missing path entry or missing pattern file?
                    return
        # print 'pattern: %s' % pattern
        return regex.compile(pattern, flags)

    def _load_pattern_file(self, filename, pattern_dict):
        with codecs.open(filename, 'r', 'utf-8') as f:
            # acc to Max this should be "lines = f.read().splitlines()"
            # because of some \r\n line breaks running with POSIX
            lines = f.readlines()
        self._load_pattern_lines(lines, pattern_dict)

    def _load_pattern_lines(self, lines, pattern_dict):
        pattern_re = regex.compile('^(?P<patname>\w+) (?P<pattern>.+)$')
        for line in lines:
            m = pattern_re.search(line)
            if m:
                md = m.groupdict()
                pattern_dict[md['patname']] = md['pattern']

    def _load_patterns(self, folders, pattern_dict=None):
        """Load all pattern from all the files in folders"""
        if pattern_dict is None:
            pattern_dict = {}
        for folder in folders:
            for file in os.listdir(folder):
                if regex.match('^[\w-]+$', file):
                    self._load_pattern_file(os.path.join(folder, file), pattern_dict)
        return pattern_dict
