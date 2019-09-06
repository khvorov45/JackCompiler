"""Top-level compiler control"""

import os
from .utilities import print_yellow, print_red

class JackCompiler:
    """Top-level control class.

    Arguments:
        jackpath = path to a single .jack file
        maxdepth = maximum recursion depth for looking for .jack files
        verbosity = verbosity of output.
    """
    # pylint: disable=attribute-defined-outside-init
    # I'm using setters/getters here, those attributes in init would look messy
    def __init__(self, jackpath=None, verbosity=None):
        self.jackpath = jackpath
        self.verbosity = verbosity

    @property
    def jackpath(self):
        """Path to .jack file"""
        return self._jackpath

    @jackpath.setter
    def jackpath(self, path):
        if path is None:
            self._jackpath = None
            return
        if not os.path.isfile(path):
            raise FileNotFoundError(".jack file not found")
        self._jackpath = path

    @property
    def verbosity(self):
        """Verbosity of output"""
        return self._verbosity

    @verbosity.setter
    def verbosity(self, opt):
        if opt is None:
            self.verbosity = "minimal"
            return
        if opt not in ["full", "minimal"]:
            raise ValueError("verbosity should be 'full' or 'minimal'")
        self._verbosity = opt

    def _create_def_outdic(self):
        """Creates the dictionary of output files"""
        outdic = {}
        outdic["tokens"] = self.jackpath.replace(".jack", "") + "T.xml"
        outdic["main"] = self.jackpath.replace(".jack", ".xml")
        return outdic

    def _read_file(self):
        """Returns a single string with all the file contents"""
        with open(self.jackpath) as jackfile:
            contents = jackfile.read()
        return contents

    def run(self):
        """Compiles one .jack file"""
        if self.jackpath is None:
            print_red("Nothing to compile")
            return
        outdic = self._create_def_outdic()
        print_yellow("Starting translation of %s" % self.jackpath)
        contents = self._read_file()
        print(contents)
