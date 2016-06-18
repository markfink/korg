# -*- coding: utf-8 -*-
from korg.korg import LineGrokker
from korg.pattern import PatternRepo


pr = PatternRepo([], True)


def test_haproxy():
    lg = LineGrokker('%{HAPROXYHTTP}', pr)

    match = lg.grok('Dec  9 13:01:26 localhost haproxy[28029]: 127.0.0.1:39759 [09/Dec/2013:12:59:46.633] loadbalancer default/instance8 0/51536/1/48082/99627 200 83285 - - ---- 87/87/87/1/0 0/67 {77.24.148.74} "GET /path/to/image HTTP/1.1"')
    assert match is not None
    assert match["program"] == "haproxy"
    assert match["client_ip"] == "127.0.0.1"
    assert match["http_verb"] == "GET" 
    assert match["server_name"] == "instance8"


def test_haproxy_iso8601_timestamp():
    lg = LineGrokker('%{HAPROXYHTTP}', pr)

    match = lg.grok('2015-08-26T02:09:48+02:00 localhost haproxy[28029]: 127.0.0.1:39759 [09/Dec/2013:12:59:46.633] loadbalancer default/instance8 0/51536/1/48082/99627 200 83285 - - ---- 87/87/87/1/0 0/67 {77.24.148.74} "GET /path/to/image HTTP/1.1"')
    assert match is not None
    assert match["program"] == "haproxy"
    assert match["client_ip"] == "127.0.0.1"
    assert match["http_verb"] == "GET" 
    assert match["server_name"] == "instance8"


def test_haproxyhttpbase():
    lg = LineGrokker('%{HAPROXYHTTPBASE}', pr)

    match = lg.grok('127.0.0.1:39759 [09/Dec/2013:12:59:46.633] loadbalancer default/instance8 0/51536/1/48082/99627 200 83285 - - ---- 87/87/87/1/0 0/67 {77.24.148.74} "GET /path/to/image HTTP/1.1"')
    assert match is not None
    assert match["client_ip"] == "127.0.0.1"
    assert match["http_verb"] == "GET" 
    assert match["server_name"] == "instance8"
