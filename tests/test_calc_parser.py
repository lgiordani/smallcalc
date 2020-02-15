from smallcalc import calc_parser as cpar


def test_parse_integer():
    p = cpar.CalcParser()
    p.lexer.load("5")

    node = p.parse_integer()

    assert node.asdict() == {
        'type': 'integer',
        'value': 5
    }


def test_parse_expression():
    p = cpar.CalcParser()
    p.lexer.load("2+3")

    node = p.parse_expression()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 2
        },
        'right': {
            'type': 'integer',
            'value': 3
        },
        'operator': {
            'type': 'literal',
            'value': '+'
        }
    }


def test_parse_expression_understands_subtraction():
    p = cpar.CalcParser()
    p.lexer.load("2-3")

    node = p.parse_expression()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 2
        },
        'right': {
            'type': 'integer',
            'value': 3
        },
        'operator': {
            'type': 'literal',
            'value': '-'
        }
    }


def test_parse_expression_with_multiple_operations():
    p = cpar.CalcParser()
    p.lexer.load("2 + 3 - 4")

    node = p.parse_expression()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 2
            },
            'right': {
                'type': 'integer',
                'value': 3
            },
            'operator': {
                'type': 'literal',
                'value': '+'
            }
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '-'
        }
    }


def test_parse_term():
    p = cpar.CalcParser()
    p.lexer.load("2 * 3")

    node = p.parse_term()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 2
        },
        'right': {
            'type': 'integer',
            'value': 3
        },
        'operator': {
            'type': 'literal',
            'value': '*'
        }
    }


def test_parse_term_with_multiple_operations():
    p = cpar.CalcParser()
    p.lexer.load("2 * 3 / 4")

    node = p.parse_term()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 2
            },
            'right': {
                'type': 'integer',
                'value': 3
            },
            'operator': {
                'type': 'literal',
                'value': '*'
            }
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '/'
        }
    }


def test_parse_expression_with_term():
    p = cpar.CalcParser()
    p.lexer.load("2 + 3 * 4")

    node = p.parse_expression()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 2
        },
        'right': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 3
            },
            'right': {
                'type': 'integer',
                'value': 4
            },
            'operator': {
                'type': 'literal',
                'value': '*'
            }
        },
        'operator': {
            'type': 'literal',
            'value': '+'
        }
    }


def test_parse_expression_with_parentheses():
    p = cpar.CalcParser()
    p.lexer.load("(2 + 3)")

    node = p.parse_expression()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'integer',
            'value': 2
        },
        'right': {
            'type': 'integer',
            'value': 3
        },
        'operator': {
            'type': 'literal',
            'value': '+'
        }
    }


def test_parse_parentheses_change_priority():
    p = cpar.CalcParser()
    p.lexer.load("(2 + 3) * 4")

    node = p.parse_expression()

    assert node.asdict() == {
        'type': 'binary',
        'left': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 2
            },
            'right': {
                'type': 'integer',
                'value': 3
            },
            'operator': {
                'type': 'literal',
                'value': '+'
            }
        },
        'right': {
            'type': 'integer',
            'value': 4
        },
        'operator': {
            'type': 'literal',
            'value': '*'
        }
    }


def test_parse_factor_supports_unary_operator():
    p = cpar.CalcParser()
    p.lexer.load("-5")

    node = p.parse_factor()

    assert node.asdict() == {
        'type': 'unary',
        'operator': {
            'type': 'literal',
            'value': '-'
        },
        'content': {
            'type': 'integer',
            'value': 5
        }
    }


def test_parse_factor_supports_negative_expressions():
    p = cpar.CalcParser()
    p.lexer.load("-(2 + 3)")

    node = p.parse_factor()

    assert node.asdict() == {
        'type': 'unary',
        'operator': {
            'type': 'literal',
            'value': '-'
        },
        'content': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 2
            },
            'right': {
                'type': 'integer',
                'value': 3
            },
            'operator': {
                'type': 'literal',
                'value': '+'
            }
        }
    }


def test_parse_factor_supports_unary_plus():
    p = cpar.CalcParser()
    p.lexer.load("+(2 + 3)")

    node = p.parse_factor()

    assert node.asdict() == {
        'type': 'unary',
        'operator': {
            'type': 'literal',
            'value': '+'
        },
        'content': {
            'type': 'binary',
            'left': {
                'type': 'integer',
                'value': 2
            },
            'right': {
                'type': 'integer',
                'value': 3
            },
            'operator': {
                'type': 'literal',
                'value': '+'
            }
        }
    }


def test_parse_factor_variable():
    p = cpar.CalcParser()
    p.lexer.load("somevar")

    node = p.parse_factor()

    assert node.asdict() == {
        'type': 'variable',
        'value': 'somevar'
    }


def test_parse_assignment():
    p = cpar.CalcParser()
    p.lexer.load("x = 5")

    node = p.parse_assignment()

    assert node.asdict() == {
        'type': 'assignment',
        'variable': 'x',
        'value': {
            'type': 'integer',
            'value': 5
        }
    }


def test_parse_assignment_with_expression():
    p = cpar.CalcParser()
    p.lexer.load("x = 4 * (3 + 5)")

    node = p.parse_assignment()

    assert node.asdict() == {
        'type': 'assignment',
        'variable': 'x',
        'value': {
            'type': 'binary',
            'operator': {
                'type': 'literal',
                'value': '*'
            },
            'left': {
                'type': 'integer',
                'value': 4
            },
            'right': {
                'type': 'binary',
                'operator': {
                    'type': 'literal',
                    'value': '+'
                },
                'left': {
                    'type': 'integer',
                    'value': 3
                },
                'right': {
                    'type': 'integer',
                    'value': 5
                }
            }
        }
    }


def test_parse_assignment_expression_with_variables():
    p = cpar.CalcParser()
    p.lexer.load("x = y + 4")

    node = p.parse_assignment()

    assert node.asdict() == {
        "type": "assignment",
        "variable": "x",
        'value': {
            'type': 'binary',
            'operator': {
                'type': 'literal',
                'value': '+'
            },
            'left': {
                'type': 'variable',
                'value': 'y'
            },
            'right': {
                'type': 'integer',
                'value': 4
            },
        }
    }
