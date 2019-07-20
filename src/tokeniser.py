"""Tokeniser class"""

from .tokeninfo import TokenInfo

class Tokeniser:
    """Creates a token list given file contents"""
    def __init__(self, file_contents, lexicon):
        self.cont = file_contents
        self.lexicon = lexicon
        self.pos = 0
        self.tokens = []
        self.cur_tok = ""
        self.tokenise()

    def tokenise(self):
        """Creates the token list"""
        inside_string = False
        for char in self.cont[self.pos:]:
            if char == '"':
                inside_string = not inside_string
            if inside_string:
                self.cur_tok += char
                continue
            if char in self.lexicon["symbols"]:
                self.add_token() # Previous token
                self.cur_tok += char
                self.add_token() # The symbol
                continue
            if not char.isspace():
                self.cur_tok += char
                continue
            else:
                self.add_token()

    def add_token(self):
        """Adds a token to the list"""
        if self.cur_tok.isspace():
            self.cur_tok = ""
            return
        if self.cur_tok == "":
            return
        self.tokens.append(TokenInfo(self.cur_tok, self.lexicon))
        self.cur_tok = ""
