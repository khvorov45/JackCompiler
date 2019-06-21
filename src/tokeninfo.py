"""TokenInfo class
"""

from .glossary import SYMBOL_ALIASES

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
        if self.toktype == "KEYWORD":
            string += (" | Keyword: {:10}".format(self.tokval))
        elif self.toktype == "SYMBOL":
            string += (" | Symbol: {:10}".format(self.tokval))
        elif self.toktype == "IDENTIFIER":
            string += (" | Identifier: {:10}".format(self.tokval))
        elif self.toktype == "INT_CONST":
            string += (" | Value: {:10}".format(str(self.tokval)))
        elif self.toktype == "STRING_CONST":
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
