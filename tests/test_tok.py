from smallcalc import tok as token


def test_token_accepts_type_and_value():
    t = token.Token("sometype", "somevalue")

    assert t.type == "sometype"
    assert t.value == "somevalue"


def test_token_transforms_value_in_string():
    t = token.Token("sometype", 3)

    assert t.type == "sometype"
    assert t.value == "3"


def test_token_keeps_value_none():
    t = token.Token("sometype", None)

    assert t.type == "sometype"
    assert t.value is None


def test_token_transforms_zero():
    t = token.Token("sometype", 0)

    assert t.type == "sometype"
    assert t.value == "0"


def test_token_value_defaults_to_none():
    t = token.Token("sometype")

    assert t.type == "sometype"
    assert t.value is None


def test_token_string_representation():
    t = token.Token("sometype", "somevalue")

    assert str(t) == "Token(sometype, 'somevalue')"


def test_token_representation():
    t = token.Token("sometype", "somevalue")

    assert repr(t) == "Token(sometype, 'somevalue')"


def test_token_equality():
    assert token.Token("sometype", "somevalue") == token.Token("sometype", "somevalue")


def test_token_equality_with_none():
    x = None
    assert token.Token("sometype", "somevalue") != x


def test_token_length():
    t = token.Token("sometype", "somevalue")

    assert len(t) == len("somevalue")
    assert bool(t) is True


def test_empty_token_has_length_zero():
    t = token.Token("sometype")

    assert len(t) == 0
    assert bool(t) is True


def test_token_accepts_text_position():
    line = 456
    column = 123
    t = token.Token("sometype", "somevalue", position=(line, column))

    assert t.type == "sometype"
    assert t.value == "somevalue"
    assert t.position == (line, column)


def test_token_equality_ignores_position():
    assert token.Token("sometype", "somevalue", position=(12, 34)) == token.Token(
        "sometype", "somevalue"
    )
    assert token.Token("sometype", "somevalue") == token.Token(
        "sometype", "somevalue", position=(12, 34)
    )


def test_token_equality_accepts_none():
    assert token.Token("sometype", "somevalue") is not None


def test_token_string_representation_with_position():
    t = token.Token("sometype", "somevalue", position=(12, 34))

    assert str(t) == "Token(sometype, 'somevalue', line=12, col=34)"
