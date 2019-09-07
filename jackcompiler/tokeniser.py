"""Tokenises the contents of a file"""

from .glossary import SYMBOL_ALIASES, SYMBOLS, KEYWORDS
from .utilities import print_red, remove_comments

class Tokeniser:
    """Creates a token list given a single string of file contents"""
    def __init__(self):
        self._contents = None
        self._tokenised = None
        self._tokens = None
        self._token_reader = TokenReader()

    @property
    def contents(self):
        """Single string of .jack file contents"""
        return self._contents

    @contents.setter
    def contents(self, contents):
        if not isinstance(contents, str):
            raise ValueError("file contents should be read as a string")
        self._contents = remove_comments(
            contents, [["//", "\n"], ["/**", "*/\n"], ["/*", "*/\n"]]
        )
        self._tokenised = False
        self._tokens = []

    def is_tokenised(self):
        """Returns the status of whether the contents have been tokenised"""
        return self._tokenised

    def get_tokens(self):
        """Returns a list of tokens"""
        if self.contents is None:
            print_red("Nothing to tokenise")
            return None
        if not self.is_tokenised():
            self.tokenise()
        return self._tokens

    def tokenise(self):
        """Creates the token list"""
        inside_string = False
        tok = ""
        for char in self.contents:
            if char == '"':
                inside_string = not inside_string
            if inside_string:
                tok += char
                continue
            if char in SYMBOLS:
                self._add_token(tok) # Previous token
                tok = ""
                self._add_token(char) # The symbol
                continue
            if not char.isspace():
                tok += char
                continue
            else:
                self._add_token(tok)
                tok = ""
        self._tokenised = True

    def _add_token(self, tok):
        """Adds a token to the list"""
        if tok.isspace():
            return
        if tok == "":
            return
        self._token_reader.token = tok
        self._tokens.append(self._token_reader.get_full_info())

class TokenReader():
    """Holds all the relevant info on the current command

    Arguments:
        token: a single element of the .jack file
    """
    def __init__(self):
        self._token = None
        self._tokval = None
        self._toktype = None

    @property
    def token(self):
        """Unaltered token"""
        return self._token

    @token.setter
    def token(self, tok):
        if not isinstance(tok, str):
            raise ValueError("token should be a string")
        self._token = tok
        self._toktype = self._get_toktype()
        self._tokval = self._get_tokval()

    def get_full_info(self):
        """Returns the dictionary of token type and value"""
        if self.token is None:
            print_red("No token")
            return None
        return {"type": self._toktype, "value": self._tokval}

    def _get_toktype(self):
        """Returns token type"""
        for keyword in KEYWORDS:
            if self.token == keyword:
                return "keyword"
        for symbol in SYMBOLS:
            if self.token == symbol:
                return "symbol"
        if self.token.isdigit():
            return "integerConstant"
        if '"' in self.token:
            return "stringConstant"
        return "identifier"

    def _get_tokval(self):
        """Returns the value of the current token"""
        if self._toktype == "intergerConstant":
            return int(self.token)
        if self._toktype == "stringConstant":
            return self.token.replace('"', "")
        if self._toktype == "symbol":
            for symbol, alias in SYMBOL_ALIASES.items():
                if self.token == symbol:
                    return self.token.replace(symbol, alias)
        return self.token
