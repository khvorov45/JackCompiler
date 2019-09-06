"""Tokenises the contents of a file"""

from .glossary import SYMBOL_ALIASES

class Tokeniser:
    """Creates a token list given a single string of file contents

    Arguments:
        file_contents: a single string of file contents
        lexicon: a dictionary with lexical elements

    """
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

class TokenInfo():
    """Holds all the relevant info on the current command

    Arguments:
        token: a single element of the .jack file
        lexicon["keywords"]: all the keywords
        lexicon["symbols"]: all the symbols

    Attributes:
        token, lexicon as above.
        toktype: token type (e.g. KEYWORD)
        tokval: token value (e.g. 'class')
    """
    def __init__(self, token, lexicon):
        self.token = token
        self.lexicon = lexicon
        self.toktype = self.get_type()
        self.tokval = self.token
        if self.toktype == "intergerConstant":
            self.tokval = int(self.token)
        if self.toktype == "stringConstant":
            self.tokval = self.token.replace('"', "")
        if self.toktype == "symbol":
            for symbol, alias in SYMBOL_ALIASES.items():
                if self.tokval == symbol:
                    self.tokval = self.tokval.replace(symbol, alias)

    def print_message(self):
        """ Prints info on the current command """

        string = ("Token: {:10} | Type: {:10}".format(
            self.token, self.toktype))
        if self.toktype == "keyword":
            string += (" | Keyword: {:10}".format(self.tokval))
        elif self.toktype == "symbol":
            string += (" | Symbol: {:10}".format(self.tokval))
        elif self.toktype == "identifier":
            string += (" | Identifier: {:10}".format(self.tokval))
        elif self.toktype == "integerConstant":
            string += (" | Value: {:10}".format(str(self.tokval)))
        elif self.toktype == "stringConstant":
            string += (" | Value: {:10}".format(self.tokval))
        else:
            raise Exception("Unexpected type")
        print(string)

    def get_type(self):
        """Returns token type"""

        keywords = self.lexicon["keywords"]
        symbols = self.lexicon["symbols"]

        for keyword in keywords:
            if self.token == keyword:
                return "keyword"

        for symbol in symbols:
            if self.token == symbol:
                return "symbol"

        if self.token.isdigit():
            return "integerConstant"

        if '"' in self.token:
            return "stringConstant"

        return "identifier"
