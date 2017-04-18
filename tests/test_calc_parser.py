from smallcalc import calc_parser as cpar


def test_parse_integer():
    p = cpar.CalcParser()
    p.lexer.load("5")

    node = p.parse_integer()

    assert node.asdict() == {
        'type': 'integer',
        'value': 5
    }
