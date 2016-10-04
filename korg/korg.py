import sys
import regex  # compared to re this implements the full regex spec like atomic grouping
from pattern import PatternRepo


# TODO: can't say if this is a useful interface. Please provide feedback if you have any thoughts.
# I use it in this way in my loganalyser
class LineGrokker(object):
    def __init__(self, pattern, pattern_repo, flags=0, callbacks=[], entries=None):
        self.regex = pattern_repo.compile_regex(pattern, flags)
        self.callbacks = callbacks
        self.entries = entries

    def grok(self, data):
        m = self.regex.search(data)
        if m:
            gd = m.groupdict()
            for c in self.callbacks:
                c(gd, self.entries)
            return gd


# this is how a sample parser (from https://github.com/kaeru-repo/plot)
# TODO: this needs testing and some docu!
def parse_lines(log_parsers, fileinp):
    """parse lines from the fileinput and send them to the log_parsers"""
    while 1:
        logentry = fileinp.readline()
        if not logentry:
            break
        elif not logentry.rstrip():
            continue  # skip newlines

        processed = False
        for lp in log_parsers:
            if lp.grok(logentry):
                processed = True
        if not processed:
            # error: none of the logparsers worked on the line
            logger = logging.getLogger('logparser')
            logger.warning(
                #'Could not parse line %s, in file %s >>>%s<<<',
                #fileinp.lineno(), fileinp.filename(), line.rstrip())
                'Could not parse line >>>%s<<<', line.rstrip())
            print 'Could not parse line >>>%s<<<' % line.rstrip()
