"""Top-level compiler control"""

class JackCompiler():
    """Top-level control class.

    Arguments:
        jackpath = path to a single .jack file
        maxdepth = maximum recursion depth for looking for .jack files
        verbosity = verbosity of output.
    """
    def __init__(
            self, jackpath, verbosity="minimal"
        ):
        self.verbosity = verbosity
        self.jackpath = jackpath

    def run(self):
        """Runs the compiler"""
        print(self.jackpath)
