"""Top-level compiler control"""

import os
from .utilities import COLOR, build_terminal
from .tokeniser import Tokeniser
from .compilationengine import CompilationEngine

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
        self._verbosity = "minimal"
        self._output = {"tokens": False, "tree": False, "vm": True}
        self._tokeniser = Tokeniser()
        self._compilationengine = CompilationEngine()

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
            "tree": path.replace(".jack", ".xml"),
            "vm": path.replace(".jack", ".vm")
        }

    @property
    def verbosity(self):
        """Verbosity of output"""
        return self._verbosity

    @verbosity.setter
    def verbosity(self, opt):
        if opt not in ["full", "minimal"]:
            raise ValueError("verbosity should be 'full' or 'minimal'")
        self._verbosity = opt

    def _out_set(self, seg, towhat):
        """Generic to set output"""
        if not isinstance(towhat, bool):
            raise ValueError(seg + "option should be boolean")
        self._output[seg] = towhat

    @property
    def outtokens(self):
        """Whether to output the tokens file"""
        return self._output["tokens"]

    @outtokens.setter
    def outtokens(self, outtokens):
        self._out_set("tokens", outtokens)

    @property
    def outtree(self):
        """Whether to output the xml tree file"""
        return self._output["tree"]

    @outtree.setter
    def outtree(self, outtree):
        self._out_set("tree", outtree)

    @property
    def outvm(self):
        """Whether to output the xml tree file"""
        return self._output["vm"]

    @outvm.setter
    def outvm(self, outvm):
        self._out_set("vm", outvm)

    def get_outdic(self):
        """Returns the output file dictionary"""
        return self._outdic

    def run(self):
        """Compiles one .jack file"""
        if self.jackpath is None:
            print(COLOR["red"] + "Nothing to compile")
            return
        print(COLOR["yellow"] + "Compiling %s" % self.jackpath)
        self._tokeniser.contents = self._contents
        toks = self._tokeniser.get_tokens()
        self._print_conditional("Tokenised successfully", "green")
        if self.outtokens:
            self._write_tokens(toks)
            self._print_conditional(
                "Wrote tokens to " + self._outdic["tokens"], "yellow"
            )
        self._compilationengine.tokens = toks
        vmcode = self._compilationengine.get_vmcode()
        self._print_conditional("Compiled to VM successfully", "green")
        if self.outtree:
            xmltree = self._compilationengine.get_xml_tree()
            self._write_string("tree", xmltree)
            self._print_conditional(
                "Wrote tree to " + self._outdic["tree"], "yellow"
            )
        if self.outvm:
            self._write_string("vm", vmcode)
            self._print_conditional(
                "Wrote vm to " + self._outdic["vm"], "yellow"
            )
        print(COLOR["yellow"] + "Finished")

    def _write_tokens(self, toks):
        """Writes the tokens"""
        with open(self._outdic["tokens"], "w+") as tokfile:
            tokfile.write("<tokens>\n")
            for tok in toks:
                tokfile.write(build_terminal(tok))
            tokfile.write("</tokens>\n")

    def _write_string(self, seg, string):
        """Writes the vm code"""
        with open(self._outdic[seg], "w+") as vmfile:
            vmfile.write(string)

    def _print_conditional(self, string, col):
        """Prints messages dependent on verbosity"""
        if self.verbosity == "minimal":
            return
        print("\t" + COLOR[col] + string)
