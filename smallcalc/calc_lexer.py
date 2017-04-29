from smallcalc import text_buffer
from smallcalc import tok as token

EOF = 'EOF'


class CalcLexer:
    def __init__(self, text=''):

        self._text_storage = text_buffer.TextBuffer(text)

    def load(self, text):
        self._text_storage.load(text)

    def get_token(self):
        self._current_token = token.Token(EOF)
        return self._current_token

    def get_tokens(self):
        return [self.get_token()]
