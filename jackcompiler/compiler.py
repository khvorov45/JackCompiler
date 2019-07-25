"""Top-level compiler control"""

class JackCompiler():
    """Top-level control class.

    Arguments:
        filepath = path to a single .jack file
        dirpath = path to a directory of .jack files
        maxdepth = maximum recursion depth for looking for .jack files
        verbosity = verbosity of output.
    """
    def __init__(
            self, filepath="", dirpath="", maxdepth=-1, verbosity="minimal"
        ):
        self.filepath = filepath
        self.dirpath = dirpath
        self.verbosity = verbosity
        self.maxdepth = maxdepth

    def run(self):
        """Runs the compiler"""
        print(self.__dict__)
