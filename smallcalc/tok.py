class Token:
    def __init__(self, _type, value=None, position=None):
        self.type = _type
        self.value = str(value) if value is not None else None
        self.position = position

    def __str__(self):
        if not self.position:
            return "Token({}, '{}')".format(self.type, self.value,)

        return "Token({}, '{}', line={}, col={})".format(
            self.type, self.value, self.position[0], self.position[1]
        )

    __repr__ = __str__

    def __eq__(self, other):
        if not other:
            return False

        return (self.type, self.value) == (other.type, other.value)

    def __len__(self):
        return len(self.value) if self.value else len(self.type)

    def __bool__(self):
        return True
