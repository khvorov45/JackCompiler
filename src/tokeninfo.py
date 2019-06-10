#--------------------------------------------------------------------------------
# TokenInfo
#--------------------------------------------------------------------------------

from glossary import *

class TokenInfo():
    """ Holds all the relevant info on the current command """
    def __init__(self, token):
        self.token = token
        self.toktype = self.get_type()
        if self.toktype == "KEYWORD":
            self.keyword = self.token
        elif self.toktype == "SYMBOL":
            self.symbol = self.token
        elif self.toktype == "IDENTIFIER":
            self.identifier = self.token
        elif self.toktype == "INT_CONST":
            self.intval = int(self.token)
        elif self.toktype == "STRING_CONST":
            self.stringval = self.token.replace('"',"")
        else: raise Exception("Unexpected type")
    
    def print_message(self):
        """ Prints info on the current command """
        string = ("Token: {:10} | Type: {:10}".format(
            self.token, self.toktype))
        if self.toktype == "KEYWORD":
            string += (" | Keyword: {:10}".format(self.keyword))
        elif self.toktype == "SYMBOL":
            string += (" | Symbol: {:10}".format(self.symbol))
        elif self.toktype == "IDENTIFIER":
            string += (" | Identifier: {:10}".format(self.identifier))
        elif self.toktype == "INT_CONST":
            string += (" | Value: {:10}".format(str(self.intval)))
        elif self.toktype == "STRING_CONST":
            string += (" | Value: {:10}".format(self.stringval))
        else: raise Exception("Unexpected type")        
        print(string)
    
    def get_type(self):
        keywords = get_glossary_lines("LexicalElements/keywords.txt")
        symbols = get_glossary_lines("LexicalElements/symbols.txt")
        
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
        