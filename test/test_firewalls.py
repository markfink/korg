# -*- coding: utf-8 -*-
from korg.korg import LineGrokker
from korg.pattern import PatternRepo


pr = PatternRepo([], True)


def test_firewalls_CISCOFW104001():
    lg = LineGrokker('%{CISCOFW104001}', pr)

    match = lg.grok("(Secondary) Switching to ACTIVE - Service card in other unit has failed")
    assert match is not None
    assert match["switch_reason"] == "Service card in other unit has failed"


def test_firewalls_CISCOFW106100():
    lg = LineGrokker('%{CISCOFW106100}', pr)

    match = lg.grok("access-list inside permitted tcp inside/10.10.123.45(51763) -> outside/192.168.67.89(80) hit-cnt 1 first hit [0x62c4905, 0x0]")
    assert match is not None
    assert match["policy_id"] == "inside"


def test_firewalls_CISCOFW106100_hyphen_in_acl():
    lg = LineGrokker('%{CISCOFW106100}', pr)

    match = lg.grok("access-list outside-entry permitted tcp outside/10.11.12.13(54726) -> inside/192.168.17.18(80) hit-cnt 1 300-second interval [0x32b3835, 0x0]")
    assert match is not None
    assert match["policy_id"] == "outside-entry"


def test_firewalls_CISCOFW106023():
    lg = LineGrokker('%{CISCOFW106023}', pr)

    match = lg.grok('Deny tcp src outside:192.168.1.1/50240 dst inside:192.168.1.2/23 by access-group "S_OUTSIDE_TO_INSIDE" [0x54c7fa80, 0x0]')
    assert match is not None
    assert match["action"] == "Deny"
    assert match["src_interface"] == "outside"
    assert match["dst_interface"] == "inside"
    assert match["protocol"] == "tcp"
    assert match["src_ip"] == "192.168.1.1"
    assert match["dst_ip"] == "192.168.1.2"
    assert match["policy_id"] == "S_OUTSIDE_TO_INSIDE"


def test_firewalls_CISCOFW106023_with_protocol_nbr():
    lg = LineGrokker('%{CISCOFW106023}', pr)

    match = lg.grok('Deny protocol 103 src outside:192.168.1.1/50240 dst inside:192.168.1.2/23 by access-group "S_OUTSIDE_TO_INSIDE" [0x54c7fa80, 0x0]')
    assert match is not None
    assert match["action"] == "Deny"
    assert match["src_interface"] == "outside"
    assert match["dst_interface"] == "inside"
    assert match["protocol"] == "103"
    assert match["src_ip"] == "192.168.1.1"
    assert match["dst_ip"] == "192.168.1.2"
    assert match["policy_id"] == "S_OUTSIDE_TO_INSIDE"


def test_firewalls_CISCOFW106023_with_hostname():
    lg = LineGrokker('%{CISCOFW106023}', pr)

    match = lg.grok('Deny tcp src outside:192.168.1.1/50240 dst inside:www.example.com/23 by access-group "S_OUTSIDE_TO_INSIDE" [0x54c7fa80, 0x0]')
    assert match is not None
    assert match["action"] == "Deny"
    assert match["src_interface"] == "outside"
    assert match["dst_interface"] == "inside"
    assert match["protocol"] == "tcp"
    assert match["src_ip"] == "192.168.1.1"
    assert match["dst_ip"] == "www.example.com"
    assert match["policy_id"] == "S_OUTSIDE_TO_INSIDE"
