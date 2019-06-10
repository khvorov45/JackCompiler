"""TokenInfo class
"""

class TokenInfo():
    """Holds all the relevant info on the current command

    Arguments:
        token: a single element of the .jack file
        lexicon["keywords"]: all the keywords
        lexicon["symbols"]: all the symbols
    """
    def __init__(self, token, lexicon):
        self.token = token
        self.lexicon = lexicon
        self.toktype = self.get_type()
        self.tokval = self.token
        if self.toktype == "INT_CONST":
            self.tokval = int(self.token)
        if self.toktype == "STRING_CONST":
            self.tokval = self.token.replace('"', "")

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
                return "KEYWORD"

        for symbol in symbols:
            if self.token == symbol:
                return "SYMBOL"

        if self.token.isdigit():
            return "INT_CONST"

        if '"' in self.token:
            return "STRING_CONST"

        return "IDENTIFIER"
