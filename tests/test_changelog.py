import textwrap

from korg import LineGrokker, PatternRepo

CHANGELOG = textwrap.dedent('''
# spec here http://keepachangelog.com/en/1.0.0/
CHANGELOG %{RELEASE}|%{TYPE}|%{CHANGE}

# sample release entry: "## [0.3.0] - 2015-12-03"
RELEASE_NUMBER \d+\.\d+\.\d+
RELEASE_DATE %{YEAR:year}-%{MONTHNUM:month}-%{MONTHDAY:day}

RELEASE ## \[%{RELEASE_NUMBER:release}\] - %{RELEASE_DATE}

# sample type entry: "### Added"
TYPE ### (?P<type>(Added|Changed|Deprecated|Removed|Fixed|Security))

# sample change entry: "- Link, and make it obvious that date format is ISO 8601."
CHANGE - (?<change>.*$)
''')

# use multilinestring for patterns parameter
PR = PatternRepo(patterns=CHANGELOG)


def test_changelog_release():
    print(PR.pattern_dict)
    lg = LineGrokker('%{RELEASE}', PR)
    expected_pattern = '## \[(?P<release>\d+\.\d+\.\d+)\] - (?P<year>(?>\d\d){1,2})-(?P<month>(?:0?[1-9]|1[0-2]))-(?P<day>(?:(?:0[1-9])|(?:[12][0-9])|(?:3[01])|[1-9]))'
    # Yee-haw
    print(lg.regex)
    #assert lg.regex.pattern == expected_pattern

    match = lg.grok('## [0.3.0] - 2015-12-03')
    # {'release': '0.3.0', 'year': '2015', 'month': '12', 'day': '03'}
    assert match is not None

    assert match['release'] == '0.3.0'
    assert match['year'] == '2015'
    assert match['month'] == '12'
    assert match['day'] == '03'


def test_changelog_type():
    lg = LineGrokker('%{TYPE}', PR)
    expected_pattern = '### (?P<type>(Added|Changed|Deprecated|Removed|Fixed|Security))'
    assert lg.regex.pattern == expected_pattern

    match = lg.grok('### Added')
    print(match)
    assert match is not None

    assert match['type'] == 'Added'


def test_changelog_change():
    lg = LineGrokker('%{CHANGE}', PR)
    assert lg.regex.pattern == '- (?<change>.*$)'

    match = lg.grok('- Link, and make it obvious that date format is ISO 8601.')
    print(match)
    assert match is not None

    assert match['change'] == 'Link, and make it obvious that date format is ISO 8601.'


def test_changelog():
    lg = LineGrokker('%{CHANGELOG}', PR)

    match = lg.grok('## [0.3.0] - 2015-12-03')
    print(match)
    assert match == \
        {'release': '0.3.0', 'year': '2015', 'month': '12', 'day': '03',
         'type': None, 'change': None}
