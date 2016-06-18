# -*- coding: utf-8 -*-
from korg.korg import LineGrokker
from korg.pattern import PatternRepo


pr = PatternRepo([], True)


def test_syslogline():
    lg = LineGrokker('%{SYSLOGLINE}', pr)

    match = lg.grok("Mar 16 00:01:25 evita postfix/smtpd[1713]: connect from camomile.cloud9.net[168.100.1.3]")
    assert match is not None  # "matches a simple message failed")
    assert match["program"] == "postfix/smtpd"  #"generates the program field failed")
    assert match["logsource"] == "evita"
    assert match["timestamp"] == "Mar 16 00:01:25"
    assert match["message"] == "connect from camomile.cloud9.net[168.100.1.3]"
    assert match["pid"] == "1713"


def test_syslogline_ietf_5424():
    lg = LineGrokker('%{SYSLOG5424LINE}', pr)

    match = lg.grok('<191>1 2009-06-30T18:30:00+02:00 paxton.local grokdebug 4123 - [id1 foo=\"bar\"][id2 baz=\"something\"] Hello, syslog.')
    assert match["syslog5424_pri"] == "191"
    assert match["syslog5424_ver"] == "1"
    assert match["syslog5424_ts"] == "2009-06-30T18:30:00+02:00"
    assert match["syslog5424_host"] == "paxton.local"
    assert match["syslog5424_app"] == "grokdebug"
    assert match["syslog5424_proc"] == "4123"
    assert match["syslog5424_msgid"] is None
    assert match["syslog5424_sd"] == "[id1 foo=\"bar\"][id2 baz=\"something\"]"
    assert match["syslog5424_msg"] == "Hello, syslog."


def test_syslogline_with_pid():
    lg = LineGrokker('%{SYSLOGLINE}', pr)

    match = lg.grok("May 11 15:17:02 meow.soy.se CRON[10973]: pam_unix(cron:session): session opened for user root by (uid=0)")
    assert match is not None  # "matches a simple message failed")


def test_syslogline_prog_with_slash():
    lg = LineGrokker('%{SYSLOGLINE}', pr)

    match = lg.grok("Mar 16 00:01:25 evita postfix/smtpd[1713]: connect from camomile.cloud9.net[168.100.1.3]")
    assert match is not None  # "matches a simple message failed")


def test_syslogline_prog_from_ansible():
    lg = LineGrokker('%{SYSLOGLINE}', pr)

    match = lg.grok("May 11 15:40:51 meow.soy.se ansible-<stdin>: Invoked with filter=* fact_path=/etc/ansible/facts.d")
    assert match is not None  # "matches a simple message failed")


def test_syslogline_optional_progname():
    lg = LineGrokker('%{SYSLOGLINE}', pr)

    match = lg.grok("<14>Jun 24 10:32:02 hostname WinFileService Event: read, Path: /.DS_Store, File/Folder: File, Size: 6.00 KB, User: user@host, IP: 123.123.123.123")
    assert match is not None  # "matches a simple message failed")
