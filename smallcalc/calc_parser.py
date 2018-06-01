from smallcalc import tok as token
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


class VariableNode(ValueNode):

    node_type = 'variable'


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


class UnaryNode(Node):

    node_type = 'unary'

    def __init__(self, operator, content):
        self.operator = operator
        self.content = content

    def asdict(self):
        result = {
            'type': self.node_type,
            'operator': self.operator.asdict(),
            'content': self.content.asdict()
        }

        return result


class PowerNode(BinaryNode):
    node_type = 'exponentiation'


class AssignmentNode(Node):

    node_type = 'assignment'

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def asdict(self):
        return {
            'type': self.node_type,
            'variable': self.variable.value,
            'value': self.value.asdict(),
        }


class CalcParser:

    def __init__(self):
        self.lexer = clex.CalcLexer()

    def _parse_literal(self, values=None):
        t = self.lexer.get_token()

        return LiteralNode(t.value)

    def parse_integer(self):
        t = self.lexer.get_token()
        return IntegerNode(t.value)

    def _parse_variable(self):
        t = self.lexer.get_token()
        return VariableNode(t.value)

    def parse_factor(self):
        next_token = self.lexer.peek_token()

        if next_token.type == clex.LITERAL and next_token.value in ['-', '+']:
            operator = self._parse_literal()
            factor = self.parse_factor()
            return UnaryNode(operator, factor)

        if next_token.type == clex.LITERAL and next_token.value == '(':
            self.lexer.discard_type(clex.LITERAL)
            expression = self.parse_expression()
            self.lexer.discard_type(clex.LITERAL)
            return expression

        if next_token.type == clex.NAME:
            t = self.lexer.get_token()
            return VariableNode(t.value)

        return self.parse_integer()

    def parse_exponentiation(self):
        left = self.parse_factor()

        next_token = self.lexer.peek_token()

        if next_token.type == clex.LITERAL and next_token.value == '^':
            operator = self._parse_literal()
            right = self.parse_exponentiation()

            return PowerNode(left, operator, right)

        return left

    def parse_term(self):
        left = self.parse_exponentiation()

        next_token = self.lexer.peek_token()

        while next_token.type == clex.LITERAL\
                and next_token.value in ['*', '/']:
            operator = self._parse_literal()
            right = self.parse_exponentiation()

            left = BinaryNode(left, operator, right)

            next_token = self.lexer.peek_token()

        return left

    def parse_expression(self):
        left = self.parse_term()

        next_token = self.lexer.peek_token()

        while next_token.type == clex.LITERAL\
                and next_token.value in ['+', '-']:
            operator = self._parse_literal()
            right = self.parse_term()

            left = BinaryNode(left, operator, right)

            next_token = self.lexer.peek_token()

        return left

    def parse_assignment(self):
        variable = self._parse_variable()
        self.lexer.discard(token.Token(clex.LITERAL, '='))
        value = self.parse_expression()

        return AssignmentNode(variable, value)

    def parse_line(self):
        with self.lexer:
            return self.parse_assignment()

        return self.parse_expression()
