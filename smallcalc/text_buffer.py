class EOLError(ValueError):

    """ Signals that the buffer is reading after the end of a line."""


class EOFError(ValueError):

    """ Signals that the buffer is reading after the end of the text."""


class TextBuffer:
    def __init__(self, text=None):
        self.load(text)

    def reset(self):
        self.line = 0
        self.column = 0

    def load(self, text):
        self.text = text
        self.lines = text.split("\n") if text else []
        self.reset()

    @property
    def current_line(self):
        try:
            return self.lines[self.line]
        except IndexError:
            raise EOFError("EOF reading line {}".format(self.line))

    @property
    def current_char(self):
        try:
            return self.current_line[self.column]
        except IndexError:
            raise EOLError(
                "EOL reading column {} at line {}".format(self.column, self.line)
            )

    @property
    def next_char(self):
        try:
            return self.current_line[self.column + 1]
        except IndexError:
            raise EOLError(
                "EOL reading column {} at line {}".format(self.column, self.line)
            )

    @property
    def tail(self):
        return self.current_line[self.column :]

    @property
    def position(self):
        return (self.line, self.column)

    def newline(self):
        self.line += 1
        self.column = 0

    def skip(self, steps=1):
        self.column += steps

    def goto(self, line, column=0):
        self.line, self.column = line, column
