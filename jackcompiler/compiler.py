"""Top-level compiler control"""

import os
from .utilities import COLOR, build_terminal
from .tokeniser import Tokeniser

class JackCompiler:
    """Top-level control class.

    Arguments:
        jackpath = path to a single .jack file
        maxdepth = maximum recursion depth for looking for .jack files
        verbosity = verbosity of output.
    """
    def __init__(self):
        self._jackpath = None
        self._contents = None
        self._outdic = None
        self._tokens = None
        self._verbosity = "minimal"
        self._outtokens = False
        self._tokeniser = Tokeniser()

    @property
    def jackpath(self):
        """Path to .jack file"""
        return self._jackpath

    @jackpath.setter
    def jackpath(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError(".jack file not found")
        self._jackpath = path
        with open(path) as jackfile:
            self._contents = jackfile.read()
        self._outdic = {
            "tokens": path.replace(".jack", "") + "T.xml",
            "main": path.replace(".jack", ".xml")
        }
        self._tokens = None

    @property
    def verbosity(self):
        """Verbosity of output"""
        return self._verbosity

    @verbosity.setter
    def verbosity(self, opt):
        if opt not in ["full", "minimal"]:
            raise ValueError("verbosity should be 'full' or 'minimal'")
        self._verbosity = opt

    @property
    def outtokens(self):
        """Whether to output the tokens file"""
        return self._outtokens

    @outtokens.setter
    def outtokens(self, outtokens):
        if not isinstance(outtokens, bool):
            raise ValueError("outtokens should be boolean")
        self._outtokens = outtokens

    def run(self):
        """Compiles one .jack file"""
        if self.jackpath is None:
            print(COLOR["red"] + "Nothing to compile")
            return
        print(COLOR["yellow"] + "Compiling %s" % self.jackpath)
        self._tokenise()
        self._print_conditional("Tokenised successfully", "green")
        if self.outtokens:
            self._print_conditional(
                "Wrote tokens to " + self._outdic["tokens"],
                "yellow"
            )
            self._write_tokens()

    def _tokenise(self):
        """Creates tokens"""
        self._tokeniser.contents = self._contents
        self._tokens = self._tokeniser.get_tokens()

    def _write_tokens(self):
        """Writes the tokens"""
        with open(self._outdic["tokens"], "w+") as tokfile:
            tokfile.write("<tokens>\n")
            for tok in self._tokens:
                tokfile.write(build_terminal(tok))
            tokfile.write("</tokens>\n")

    def _print_conditional(self, string, col):
        """Prints messages dependent on verbosity"""
        if self.verbosity == "minimal":
            return
        print("\t" + COLOR[col] + string)
