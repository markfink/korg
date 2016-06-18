from nose.tools import istest as test
from nose.tools import nottest
from pyvows import Vows, expect
from korg.korg import LineGrokker
from korg.pattern import PatternRepo

# TODO testcases
#

# test helpers
@Vows.create_assertions
def has_element(topic, expected):
    return expected in topic

@Vows.create_assertions
def not_has_element(topic, expected):
    return not(expected in topic)


def test_pattern_not_found():
    pr = PatternRepo([], True)
    lg = LineGrokker('%{UNKNOWN}', pr)
    assert lg.regex == None


# test samples taken from logstash/spec/filters/grok.rb v1.1.13
"""
  describe "parsing an event with multiple messages (array of strings)" do
    config <<-CONFIG
      filter {
        grok {
          pattern => "(?:hello|world) %{NUMBER}"
          named_captures_only => false
        }
      }
    CONFIG

    sample({ "@message" => [ "hello 12345", "world 23456" ] }) do
      insist { subject["NUMBER"] } == [ "12345", "23456" ]
    end
  end

  describe "coercing matched values" do
    config <<-CONFIG
      filter {
        grok {
          pattern => "%{NUMBER:foo:int} %{NUMBER:bar:float}"
          singles => true
        }
      }
    CONFIG

    sample "400 454.33" do
      insist { subject["foo"] } == 400
      insist { subject["foo"] }.is_a?(Fixnum)
      insist { subject["bar"] } == 454.33
      insist { subject["bar"] }.is_a?(Float)
    end
  end

  describe "in-line pattern definitions" do
    config <<-CONFIG
      filter {
        grok {
          pattern => "%{FIZZLE=\\d+}"
          named_captures_only => false
          singles => true
        }
      }
    CONFIG

    sample "hello 1234" do
      insist { subject["FIZZLE"] } == "1234"
    end
  end

  describe "processing fields other than @message" do
    config <<-CONFIG
      filter {
        grok {
          pattern => "%{WORD:word}"
          match => [ "examplefield", "%{NUMBER:num}" ]
          break_on_match => false
          singles => true
        }
      }
    CONFIG

    sample({ "@message" => "hello world", "@fields" => { "examplefield" => "12345" } }) do
      insist { subject["examplefield"] } == "12345"
      insist { subject["word"] } == "hello"
    end
  end

  describe "adding fields on match" do
    config <<-CONFIG
      filter {
        grok {
          pattern => "matchme %{NUMBER:fancy}"
          singles => true
          add_field => [ "new_field", "%{fancy}" ]
        }
      }
    CONFIG

    sample "matchme 1234" do
      reject { subject["@tags"] }.include?("_grokparsefailure")
      insist { subject["new_field"] } == ["1234"]
    end

    sample "this will not be matched" do
      insist { subject["@tags"] }.include?("_grokparsefailure")
      reject { subject }.include?("new_field")
    end
  end
"""

# empty fields

@nottest
def it_drops_empty_fields_by_default():
    # not implemented
    pr = PatternRepo(['patterns/'])
    g = LineGrokker('1=%{WORD:foo1} *(2=%{WORD:foo2})?', pr)

    subject = g.grok('1=test')

    expect(subject).has_element("foo1")
    # Since 'foo2' was not captured, it must not be present in the event.
    expect(subject).not_has_element("foo2")


@test
def it_keep_empty_fields():
    pr = PatternRepo(['patterns/'])
    g = LineGrokker('1=%{WORD:foo1} *(2=%{WORD:foo2})?', pr)

    subject = g.grok('1=test')

    expect(subject).has_element("foo1")
    # Since 'foo2' was not captured, it must not be present in the event.
    expect(subject).has_element("foo2")
    expect(subject["foo2"]).to_equal(None)

"""
  describe "when named_captures_only == false" do
    config <<-CONFIG
      filter {
        grok {
          pattern => "Hello %{WORD}. %{WORD:foo}"
          named_captures_only => false
          singles => true
        }
      }
    CONFIG

    sample "Hello World, yo!" do
      insist { subject }.include?("WORD")
      insist { subject["WORD"] } == "World"
      insist { subject }.include?("foo")
      insist { subject["foo"] } == "yo"
    end
  end
"""


@test
def it_uses_named_captures():
    pr = PatternRepo(['patterns/'])
    g = LineGrokker('(?<foo>\w+)', pr)

    subject = g.grok('hello world')

    print 'subject: %s' % subject
    expect(subject["foo"]).to_equal("hello")


@test
def it_groks_patterns():
    pr = PatternRepo(['patterns/'])
    g = LineGrokker('(?<timestamp>%{DATE_EU} %{TIME})', pr)

    subject = g.grok('fancy 2001-02-03 04:05:06')

    print 'subject: %s' % subject
    expect(subject["timestamp"]).to_equal("01-02-03 04:05:06")


"""
  describe "grok on integer types" do
    config <<-'CONFIG'
      filter {
        grok {
          match => [ "status", "^403$" ]
          add_tag => "four_oh_three"
        }
      }
    CONFIG

    sample({ "@fields" => { "status" => 403 } }) do
      reject { subject.tags }.include?("_grokparsefailure")
      insist { subject.tags }.include?("four_oh_three")
    end
  end

  describe "grok on float types" do
    config <<-'CONFIG'
      filter {
        grok {
          match => [ "version", "^1.0$" ]
          add_tag => "one_point_oh"
        }
      }
    CONFIG

    sample({ "@fields" => { "version" => 1.0 } }) do
      reject { subject.tags }.include?("_grokparsefailure")
      insist { subject.tags }.include?("one_point_oh")
    end
  end


  describe "tagging on failure" do
    config <<-CONFIG
      filter {
        grok {
          pattern => "matchme %{NUMBER:fancy}"
          tag_on_failure => false
        }
      }
    CONFIG

    sample "matchme 1234" do
      reject { subject["@tags"] }.include?("_grokparsefailure")
    end

    sample "this will not be matched" do
      reject { subject["@tags"] }.include?("_grokparsefailure")
    end
  end


end
"""

@test
def it_captures_named_fields_even_if_the_whole_text_matches():
    pr = PatternRepo(['patterns/'])
    g = LineGrokker('%{DATE_EU:stimestamp}', pr)

    subject = g.grok('2011/01/01')

    print 'subject: %s' % subject
    expect(subject["stimestamp"]).to_equal("11/01/01")

@nottest
def test_allows_dashes_in_capture_names():
    # not implemented
    pr = PatternRepo(['patterns/'])
    g = LineGrokker('%{WORD:foo-bar}', pr)

    subject = g.grok('hello world')

    print 'subject: %s' % subject
    expect(subject["foo-bar"]).to_equal("hello")
