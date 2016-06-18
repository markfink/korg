# -*- coding: utf-8 -*-
from korg.korg import LineGrokker
from korg.pattern import PatternRepo


pr = PatternRepo([], True)


def test_commonapachelog():
    lg = LineGrokker('%{COMMONAPACHELOG}', pr)

    match = lg.grok('83.149.9.216 - - [24/Feb/2015:23:13:42 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36')
    assert match is not None
    assert match["clientip"] == "83.149.9.216"


def test_httpdate_german_month():
    lg = LineGrokker('%{HTTPDATE}', pr)

    match = lg.grok('[04/Mai/2015:13:17:15 +0200]')
    assert match is not None


def test_httpdate_english_month():
    lg = LineGrokker('%{HTTPDATE}', pr)

    match = lg.grok('[04/March/2015:13:17:15 +0200]')
    assert match is not None


def test_httpdate_wrong_month():
    lg = LineGrokker('%{HTTPDATE}', pr)

    match = lg.grok('[04/Map/2015:13:17:15 +0200]')
    assert match is None


# move to java
def test_tomcatlog():
    lg = LineGrokker('%{TOMCATLOG}', pr)

    match = lg.grok('2014-01-09 20:03:28,269 -0800 | ERROR | com.example.service.ExampleService - something compeletely unexpected happened...')
    assert match is not None
    assert match["logmessage"] == "something compeletely unexpected happened..."


def test_iporhost_matching_ip():
    lg = LineGrokker('%{IPORHOST}', pr)

    match = lg.grok('127.0.0.1')
    assert match is not None


def test_iporhost_matching_host():
    lg = LineGrokker('%{IPORHOST}', pr)

    match = lg.grok('example.org')
    assert match is not None


def test_unixpath():
    lg = LineGrokker('%{UNIXPATH}', pr)

    match = lg.grok('/foo/bar')
    assert match is not None


def test_unixpath_using_comma_and_other_regex_excapes():
    lg = LineGrokker('%{UNIXPATH}', pr)

    match = lg.grok('a=/some/path, b=/some/other/path')
    assert match is not None


def test_uripath():
    lg = LineGrokker('%{URIPATH}', pr)

    match = lg.grok('/foo')
    assert match is not None


def test_uripath_trailing_slash():
    lg = LineGrokker('%{URIPATH}', pr)

    match = lg.grok('/foo/')
    assert match is not None


def test_uripath_multiple_levels():
    lg = LineGrokker('%{URIPATH}', pr)

    match = lg.grok('/foo/bar')
    assert match is not None


def test_uripath_fancy_characters():
    lg = LineGrokker('%{URIPATH}', pr)

    match = lg.grok('/aA1$.+!*\'(){},~:;=@#%&|-')
    assert match is not None


def test_uripath_invalid_uri():
    lg = LineGrokker('%{URIPATH}', pr)

    match = lg.grok('foo')
    assert match is None


def test_ipv4():
    lg = LineGrokker('%{IPV4}', pr)

    match = lg.grok('127.0.0.1')
    assert match is not None


def test_ipv4_local_ip():
    lg = LineGrokker('%{IPV4}', pr)

    match = lg.grok('10.0.0.1')
    assert match is not None


def test_ipv4_wrong_ip():
    lg = LineGrokker('%{IPV4}', pr)

    match = lg.grok('192.300.300.300')
    assert match is None


def test_urn_valid():
    lg = LineGrokker('%{URN}', pr)

    assert lg.grok("urn:example:foo") is not None
    assert lg.grok("urn:example:/#?") is not None
    assert lg.grok("urn:example:%25foo%2Fbar%3F%23") is not None
    assert lg.grok("urn:example:%25foo%2fbar%3f%23") is not None
    assert lg.grok("urn:example:%00") is not None
    assert lg.grok("urn:example-example-example-example-:foo") is not None

def test_urn_invalid():
    lg = LineGrokker('%{URN}', pr)

    assert lg.grok("URN:example:foo") is None
    assert lg.grok("urn::foo") is None
    assert lg.grok("urn:-example:foo") is None
    assert lg.grok("urn:example.com:foo") is None
    assert lg.grok("urn:example%41com:foo") is None
    assert lg.grok("urn:example-example-example-example-x:foo") is None
    assert lg.grok("urn:example:") is None
    assert lg.grok("urn:example:%") is None
    assert lg.grok("urn:example:%a") is None
    assert lg.grok("urn:example:%ax") is None
