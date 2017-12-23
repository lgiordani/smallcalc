from smallcalc import calc_lexer as clex


class Node:

    def asdict(self):
        return {}  # pragma: no cover


class ValueNode(Node):

    node_type = 'value_node'

    def __init__(self, value):
        self.value = value

    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.value
        }


class IntegerNode(ValueNode):
    node_type = 'integer'

    def __init__(self, value):
        self.value = int(value)


class LiteralNode(ValueNode):

    node_type = 'literal'


class BinaryNode(Node):

    node_type = 'binary'

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def asdict(self):
        result = {
            'type': self.node_type,
            'left': self.left.asdict()
        }

        result['right'] = None
        if self.right:
            result['right'] = self.right.asdict()

        result['operator'] = None
        if self.operator:
            result['operator'] = self.operator.asdict()

        return result


class CalcParser:

    def __init__(self):
        self.lexer = clex.CalcLexer()

    def parse_addsymbol(self):
        t = self.lexer.get_token()
        return LiteralNode(t.value)

    def parse_integer(self):
        t = self.lexer.get_token()
        return IntegerNode(t.value)

    def parse_term(self):
        left = self.parse_integer()

        next_token = self.lexer.peek_token()

        while next_token.type == clex.LITERAL:
            operator = self.parse_addsymbol()
            right = self.parse_integer()

            left = BinaryNode(left, operator, right)

            next_token = self.lexer.peek_token()

        return left

    def parse_expression(self):
        left = self.parse_integer()

        next_token = self.lexer.peek_token()

        while next_token.type == clex.LITERAL:
            operator = self.parse_addsymbol()
            right = self.parse_integer()

            left = BinaryNode(left, operator, right)

            next_token = self.lexer.peek_token()

        return left
