from smallcalc import tok as token
from smallcalc import calc_lexer as clex


def test_get_tokens_understands_eof():
    l = clex.CalcLexer()

    l.load('')

    assert l.get_tokens() == [
        token.Token(clex.EOF)
    ]
