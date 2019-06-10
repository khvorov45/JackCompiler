#--------------------------------------------------------------------------------
# JackCompiler control class
#--------------------------------------------------------------------------------

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from glossary import get_full_indicator
from print_utils import print_padded

class JackCompiler():
    """ Controls compilation """
    def __init__(self, args):
        self.filepaths = args.filepaths
        self.verbosity = args.verbosity
    
    def run(self):
        """ Main method to run the compilation process """
        for filepath in self.filepaths:
            self.print_start_msg(filepath)
            
            out_path = filepath.replace(".jack",".xml")
            tokens = JackTokenizer(filepath).contents
            
            if self.verbosity == get_full_indicator():
                for token in tokens: token.print_message()
            
            writer = CompilationEngine(tokens, out_path)
            writer.compile_class()
            
            self.print_end_msg(out_path)
    
    def print_start_msg(self, file_name):
        """ Prints start message """
        print_padded("Starting translation of %s" % file_name)
    
    
    def print_end_msg(self, file_name):
        """ Prints end message """
        print_padded("Wrote translation to %s" % (file_name))    