import pytest

from smallcalc import text_buffer


def test_text_buffer_init_empty():
    tb = text_buffer.TextBuffer()

    with pytest.raises(text_buffer.EOFError):
        tb.current_char


def test_text_buffer_init_one_line():
    tb = text_buffer.TextBuffer("abcdef")

    assert tb.current_char == "a"
    assert tb.next_char == "b"
    assert tb.current_line == "abcdef"
    assert tb.line == 0
    assert tb.column == 0


def test_text_buffer_end_of_line_next_char():
    tb = text_buffer.TextBuffer("abcdef")
    tb.column = 5

    assert tb.current_char == "f"
    with pytest.raises(text_buffer.EOLError):
        tb.next_char


def test_text_buffer_end_of_line_current_char():
    tb = text_buffer.TextBuffer("abcdef")
    tb.column = 200

    with pytest.raises(text_buffer.EOLError):
        tb.current_char


def test_text_buffer_error_at_end_of_file():
    tb = text_buffer.TextBuffer("abcdef")
    tb.line = 1

    with pytest.raises(text_buffer.EOFError):
        tb.current_line


def test_text_buffer_error_after_end_of_file():
    tb = text_buffer.TextBuffer("abcdef")
    tb.line = 100

    with pytest.raises(text_buffer.EOFError):
        tb.current_line


def test_text_buffer_tail():
    ts = text_buffer.TextBuffer("abcdefgh")
    ts.column = 4

    assert ts.tail == "efgh"


def test_text_buffer_multiple_lines():
    tb = text_buffer.TextBuffer("abc\ndef\nghi")
    tb.line = 1
    tb.column = 1

    assert tb.current_line == "def"
    assert tb.current_char == "e"
    assert tb.next_char == "f"


def test_text_buffer_newline():
    tb = text_buffer.TextBuffer("abc\ndef\nghi")
    tb.line = 1
    tb.column = 2
    tb.newline()

    assert tb.position == (2, 0)


def test_text_buffer_position():
    tb = text_buffer.TextBuffer()
    tb.line = 123
    tb.column = 456

    assert tb.position == (123, 456)


def test_text_buffer_skip_defaults_to_one():
    tb = text_buffer.TextBuffer("abc\ndef\nghi")
    tb.skip()

    assert tb.column == 1


def test_text_buffer_skip_accepts_value():
    tb = text_buffer.TextBuffer("abc\ndef\nghi")
    tb.skip(3)

    assert tb.column == 3


def test_text_buffer_goto():
    tb = text_buffer.TextBuffer()
    tb.goto(12, 45)

    assert tb.position == (12, 45)


def test_text_buffer_goto_default_column():
    tb = text_buffer.TextBuffer()
    tb.goto(12)

    assert tb.position == (12, 0)
