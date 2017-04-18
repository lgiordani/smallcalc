class CalcVisitor:

    def visit(self, node):
        if node['type'] == 'integer':
            return node['value'], node['type']
