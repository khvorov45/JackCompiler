#--------------------------------------------------------------------------------
# JackTokenizer class
#--------------------------------------------------------------------------------

from print_utils import *
from glossary import get_glossary_lines
from TokenInfo import TokenInfo

class JackTokenizer():
    """ Handles tokenising of input """
    def __init__(self, jackfile_path):
        with open(jackfile_path, 'r') as jackfile:
            self.contents = jackfile.read()
        self._remove_comments([["//","\n"], ["/**","*/"], ["/*","*/"]])
        self._add_whitespaces()
        self._unify_strings()
        self.fill_info()
    
    def fill_info(self):
        """ Adds the required info on each token """
        tokens = self.contents
        tokens = [TokenInfo(token) for token in tokens]
        self.contents = tokens
    
    def _unify_strings(self):
        """ Unify string literals into a single token """
        tokens = self.contents.split()
        tokens_new = []
        inside_string = False
        
        for token in tokens:
            
            if inside_string:
                tokens_new[-1] += " "+token
            else: tokens_new.append(token)
            
            if '"' in token:
                inside_string = not inside_string

        self.contents = tokens_new
    
    def _add_whitespaces(self):
        """ Adds whitespaces around symbols """
        symbols = get_glossary_lines("LexicalElements/symbols.txt")
        for symbol in symbols:
            if symbol in self.contents:
                self.contents = self.contents.replace(symbol, " "+symbol+" ")
    
    def _remove_comments(self, comment_breaks):
        """ Removes all of the comments from a string """
        string = self.contents
        
        for com_set in comment_breaks:
            opener = com_set[0]
            closer = com_set[1]
            
            while opener in string: 
                ind_start = string.index(opener)
                
                keep_left = string[:ind_start]
                rest = string[ind_start:]
                if closer == "\n":
                    keep_right = rest[ rest.index(closer) : ]
                else: keep_right = rest[ rest.index(closer) + len(closer) : ]
                string = keep_left + keep_right        
        
        self.contents = string