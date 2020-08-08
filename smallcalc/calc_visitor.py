class CalcVisitor:
    def __init__(self):
        self.variables = {}

    def isvariable(self, name):
        return name in self.variables

    def valueof(self, name):
        return self.variables[name]["value"]

    def typeof(self, name):
        return self.variables[name]["type"]

    def visit(self, node):
        if node["type"] in ["integer", "float"]:
            return node["value"], node["type"]

        if node["type"] == "variable":
            return self.valueof(node["value"]), self.typeof(node["value"])

        if node["type"] == "unary":
            operator = node["operator"]["value"]
            cvalue, ctype = self.visit(node["content"])

            if operator == "-":
                return -cvalue, ctype

            return cvalue, ctype

        if node["type"] == "binary":
            lvalue, ltype = self.visit(node["left"])
            rvalue, rtype = self.visit(node["right"])

            operator = node["operator"]["value"]

            if ltype == "float":
                rtype = ltype

            if operator == "+":
                return lvalue + rvalue, rtype
            elif operator == "-":
                return lvalue - rvalue, rtype
            elif operator == "*":
                return lvalue * rvalue, rtype
            elif operator == "/":
                return lvalue // rvalue, rtype

        if node["type"] == "assignment":
            right_value, right_type = self.visit(node["value"])
            self.variables[node["variable"]] = {
                "value": right_value,
                "type": right_type,
            }

            return None, None

        if node["type"] == "exponentiation":
            lvalue, ltype = self.visit(node["left"])
            rvalue, rtype = self.visit(node["right"])

            return lvalue ** rvalue, ltype
