"""JackCompiler control class
"""

#from JackTokenizer import JackTokenizer
#from CompilationEngine import CompilationEngine
#from glossary import get_full_indicator
#from print_utils import print_padded

class JackCompiler():
    """Controls compilation

    Arguments and attributes:
        lexicon: a dictionary with keywords and symbols
        jack_files: a list with filepaths to the .jack files to be compiled
        verbosity: verbosity of output. "full" or "minimal".
    """
    def __init__(self, lexicon, jack_files, verbosity):
        self.lexicon = lexicon
        self.jack_files = jack_files
        self.verbosity = verbosity

    def run(self):
        """ Main method to run the compilation process """
        for jack_file in self.jack_files:
            self.print_start_msg(jack_file)

            out_path = jack_file.replace(".jack", ".xml")
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