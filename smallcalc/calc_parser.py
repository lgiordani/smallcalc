from smallcalc import tok as token
from smallcalc import calc_lexer as clex


class Node:
    def asdict(self):
        return {}  # pragma: no cover


class ValueNode(Node):

    node_type = "value_node"

    def __init__(self, value):
        self.value = value

    def asdict(self):
        return {"type": self.node_type, "value": self.value}


class IntegerNode(ValueNode):
    node_type = "integer"

    def __init__(self, value):
        self.value = int(value)


class FloatNode(ValueNode):
    node_type = "float"


class LiteralNode(ValueNode):

    node_type = "literal"


class VariableNode(ValueNode):

    node_type = "variable"


class BinaryNode(Node):

    node_type = "binary"

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def asdict(self):
        result = {"type": self.node_type, "left": self.left.asdict()}

        result["right"] = None
        if self.right:
            result["right"] = self.right.asdict()

        result["operator"] = None
        if self.operator:
            result["operator"] = self.operator.asdict()

        return result


class UnaryNode(Node):

    node_type = "unary"

    def __init__(self, operator, content):
        self.operator = operator
        self.content = content

    def asdict(self):
        result = {
            "type": self.node_type,
            "operator": self.operator.asdict(),
            "content": self.content.asdict(),
        }

        return result


class PowerNode(BinaryNode):
    node_type = "exponentiation"


class AssignmentNode(Node):

    node_type = "assignment"

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def asdict(self):
        return {
            "type": self.node_type,
            "variable": self.variable.value,
            "value": self.value.asdict(),
        }


class CalcParser:
    def __init__(self):
        self.lexer = clex.CalcLexer()

    def _parse_literal(self, values=None):
        t = self.lexer.get_token()

        if t.type != clex.LITERAL:
            raise clex.TokenError

        if values and t.value not in values:
            raise clex.TokenError

        return LiteralNode(t.value)

    def parse_number(self):
        t = self.lexer.get_token()

        if t.type == clex.INTEGER:
            return IntegerNode(int(t.value))
        elif t.type == clex.FLOAT:
            return FloatNode(float(t.value))

        raise clex.TokenError

    def _parse_variable(self):
        t = self.lexer.get_token()

        if t.type != clex.NAME:
            raise clex.TokenError

        return VariableNode(t.value)

    def parse_factor(self):
        with self.lexer:
            operator = self._parse_literal(["+", "-"])
            content = self.parse_factor()
            return UnaryNode(operator, content)

        with self.lexer:
            self._parse_literal(["("])
            expression = self.parse_expression()
            self._parse_literal([")"])
            return expression

        with self.lexer:
            return self._parse_variable()

        return self.parse_number()

    def parse_exponentiation(self):
        left = self.parse_factor()

        with self.lexer:
            operator = self._parse_literal(["^"])
            right = self.parse_exponentiation()

            return PowerNode(left, operator, right)

        return left

    def parse_term(self):
        left = self.parse_exponentiation()

        with self.lexer:
            operator = self._parse_literal(["*", "/"])
            right = self.parse_term()

            return BinaryNode(left, operator, right)

        return left

    def parse_expression(self):
        left = self.parse_term()

        with self.lexer:
            operator = self._parse_literal(["+", "-"])
            right = self.parse_expression()

            left = BinaryNode(left, operator, right)

        return left

    def parse_assignment(self):
        variable = self._parse_variable()
        self.lexer.discard(token.Token(clex.LITERAL, ":"))
        self.lexer.discard(token.Token(clex.LITERAL, "="))
        value = self.parse_expression()

        return AssignmentNode(variable, value)

    def parse_line(self):
        with self.lexer:
            return self.parse_assignment()

        return self.parse_expression()
