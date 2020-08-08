import pytest

from smallcalc import tok as token
from smallcalc import calc_lexer as clex


def test_get_tokens_understands_eof():
    l = clex.CalcLexer()

    l.load("")

    assert l.get_tokens() == [token.Token(clex.EOF)]


def test_get_token_understands_integers():
    l = clex.CalcLexer()

    l.load("3")

    assert l.get_token() == token.Token(clex.INTEGER, "3")


def test_get_tokens_understands_integers():
    l = clex.CalcLexer()

    l.load("3")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_unspaced_sum_of_integers():
    l = clex.CalcLexer()

    l.load("3+5")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.LITERAL, "+"),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_multiple_digits():
    l = clex.CalcLexer()

    l.load("356")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "356"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_ignores_spaces():
    l = clex.CalcLexer()

    l.load("3 + 5")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.LITERAL, "+"),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_subtraction():
    l = clex.CalcLexer()

    l.load("3 - 5")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.LITERAL, "-"),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_multiple_operations():
    l = clex.CalcLexer()

    l.load("3 + 5 - 7")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.LITERAL, "+"),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.LITERAL, "-"),
        token.Token(clex.INTEGER, "7"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_lexer_can_stash_and_pop_status():
    l = clex.CalcLexer()
    l.load("3 5")

    l.stash()
    l.get_token()
    l.pop()

    assert l.get_token() == token.Token(clex.INTEGER, "3")


def test_lexer_can_peek_token():
    l = clex.CalcLexer()
    l.load("3 + 5")

    l.get_token()
    assert l.peek_token() == token.Token(clex.LITERAL, "+")


def test_get_tokens_understands_multiplication():
    l = clex.CalcLexer()

    l.load("3 * 5")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.LITERAL, "*"),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_division():
    l = clex.CalcLexer()

    l.load("3 / 5")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.LITERAL, "/"),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_parentheses():
    l = clex.CalcLexer()

    l.load("3 * ( 5 + 7 )")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.LITERAL, "*"),
        token.Token(clex.LITERAL, "("),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.LITERAL, "+"),
        token.Token(clex.INTEGER, "7"),
        token.Token(clex.LITERAL, ")"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_discard_tokens():
    l = clex.CalcLexer()
    l.load("3 + 5")

    l.discard(token.Token(clex.INTEGER, "3"))
    assert l.get_token() == token.Token(clex.LITERAL, "+")


def test_discard_checks_equality():
    l = clex.CalcLexer()
    l.load("3 + 5")

    with pytest.raises(clex.TokenError):
        l.discard(token.Token(clex.INTEGER, "5"))


def test_discard_tokens_by_type():
    l = clex.CalcLexer()
    l.load("3 + 5")

    l.discard_type(clex.INTEGER)
    assert l.get_token() == token.Token(clex.LITERAL, "+")


def test_discard_type_checks_equality():
    l = clex.CalcLexer()
    l.load("3 + 5")

    with pytest.raises(clex.TokenError):
        l.discard_type(clex.LITERAL)


def test_get_tokens_understands_letters():
    l = clex.CalcLexer()

    l.load("somevar")

    assert l.get_tokens() == [
        token.Token(clex.NAME, "somevar"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_uppercase_letters():
    l = clex.CalcLexer()

    l.load("SomeVar")

    assert l.get_tokens() == [
        token.Token(clex.NAME, "SomeVar"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_names_with_underscores():
    l = clex.CalcLexer()

    l.load("some_var")

    assert l.get_tokens() == [
        token.Token(clex.NAME, "some_var"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_exponentiation():
    l = clex.CalcLexer()

    l.load("2 ^ 3")

    assert l.get_tokens() == [
        token.Token(clex.INTEGER, "2"),
        token.Token(clex.LITERAL, "^"),
        token.Token(clex.INTEGER, "3"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_lexer_as_context_manager():
    l = clex.CalcLexer()
    l.load("abcd")

    with l:
        assert l.get_token() == token.Token(clex.NAME, "abcd")


def test_lexer_as_context_manager_does_not_restore_the_status_if_no_error():
    l = clex.CalcLexer()
    l.load("3 * 5")

    with l:
        assert l.get_token() == token.Token(clex.INTEGER, 3)

    assert l.get_token() == token.Token(clex.LITERAL, "*")


def test_lexer_as_context_manager_restores_the_status_if_token_error():
    l = clex.CalcLexer()
    l.load("3 * 5")

    with l:
        l.get_token()
        l.get_token()
        raise clex.TokenError

    assert l.get_token() == token.Token(clex.INTEGER, 3)


def test_get_tokens_understands_floats():
    l = clex.CalcLexer()

    l.load("3.6")

    assert l.get_tokens() == [
        token.Token(clex.FLOAT, "3.6"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_begin_and_end():
    l = clex.CalcLexer()

    l.load("BEGIN END")

    assert l.get_tokens() == [
        token.Token(clex.BEGIN),
        token.Token(clex.END),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_final_dot():
    l = clex.CalcLexer()

    l.load("BEGIN END.")

    assert l.get_tokens() == [
        token.Token(clex.BEGIN),
        token.Token(clex.END),
        token.Token(clex.DOT),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]


def test_get_tokens_understands_assignment_and_semicolon():
    l = clex.CalcLexer()

    l.load("a := 5;")

    assert l.get_tokens() == [
        token.Token(clex.NAME, "a"),
        token.Token(clex.LITERAL, ":"),
        token.Token(clex.LITERAL, "="),
        token.Token(clex.INTEGER, "5"),
        token.Token(clex.LITERAL, ";"),
        token.Token(clex.EOL),
        token.Token(clex.EOF),
    ]
