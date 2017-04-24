import re

from smallcalc import text_buffer
from smallcalc import tok as token

EOF = 'EOF'
EOL = 'EOL'
INTEGER = 'INTEGER'
LITERAL = 'LITERAL'
NAME = 'NAME'


class TokenError(ValueError):

    """ The expected token cannot be found """


class CalcLexer:

    def __init__(self, text=''):
        self._text_storage = text_buffer.TextBuffer(text)
        self._status = []
        self._current_token = None

    def load(self, text):
        self._text_storage.load(text)

    @property
    def _current_char(self):
        return self._text_storage.current_char

    @property
    def _current_line(self):
        return self._text_storage.current_line

    @property
    def _current_status(self):
        status = {}
        status['text_storage'] = self._text_storage.position
        status['current_token'] = self._current_token
        return status

    def stash(self):
        self._status.append(self._current_status)

    def pop(self):
        status = self._status.pop()
        self._text_storage.goto(*status['text_storage'])
        self._current_token = status['current_token']

    def _set_current_token_and_skip(self, token):
        self._text_storage.skip(len(token))

        self._current_token = token
        return token

    def _process_eol(self):
        try:
            self._current_char
            return None
        except text_buffer.EOLError:
            self._text_storage.newline()

            return self._set_current_token_and_skip(
                token.Token(EOL)
            )

    def _process_eof(self):
        try:
            self._current_line
            return None
        except text_buffer.EOFError:
            return self._set_current_token_and_skip(
                token.Token(EOF)
            )

    def _process_whitespace(self):
        regexp = re.compile('\ +')

        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        self._text_storage.skip(len(match.group()))

    def _process_literal(self):
        return self._set_current_token_and_skip(
            token.Token(LITERAL, self._current_char)
        )

    def _process_integer(self):
        regexp = re.compile('\d+')

        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()

        return self._set_current_token_and_skip(
            token.Token(INTEGER, int(token_string))
        )

    def _process_name(self):
        regexp = re.compile('[a-z]+')

        match = regexp.match(
            self._text_storage.tail
        )

        if not match:
            return None

        token_string = match.group()

        return self._set_current_token_and_skip(
            token.Token(NAME, token_string)
        )

    def discard(self, token):
        if self.get_token() != token:
            raise TokenError(
                'Expected token {}, found {}'.format(
                    token, self._current_token
                ))

    def discard_type(self, _type):
        t = self.get_token()

        if t.type != _type:
            raise TokenError(
                'Expected token of type {}, found {}'.format(
                    _type, self._current_token.type
                ))

    def get_token(self):
        eof = self._process_eof()
        if eof:
            return eof

        eol = self._process_eol()
        if eol:
            return eol

        self._process_whitespace()

        name = self._process_name()
        if name:
            return name

        integer = self._process_integer()
        if integer:
            return integer

        literal = self._process_literal()
        if literal:
            return literal

    def get_tokens(self):
        t = self.get_token()
        tokens = []

        while t != token.Token('EOF'):
            tokens.append(t)
            t = self.get_token()

        tokens.append(token.Token('EOF'))

        return tokens

    def peek_token(self):
        self.stash()
        token = self.get_token()
        self.pop()

        return token
