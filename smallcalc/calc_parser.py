from smallcalc import calc_lexer as clex


class IntegerNode:
    node_type = 'integer'

    def __init__(self, value):
        self.value = int(value)

    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.value
        }


class CalcParser:

    def __init__(self):
        self.lexer = clex.CalcLexer()

    def parse_integer(self):
        t = self.lexer.get_token()
        return IntegerNode(t.value)
