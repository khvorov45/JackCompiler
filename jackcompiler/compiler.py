"""Top-level compiler control"""

from .utilities import print_yellow

class JackCompiler:
    """Top-level control class.

    Arguments:
        jackpath = path to a single .jack file
        maxdepth = maximum recursion depth for looking for .jack files
        verbosity = verbosity of output.
    """
    # pylint: disable=attribute-defined-outside-init
    # I'm using setters/getters here, those attributes in init would look messy
    def __init__(
            self, jackpath, verbosity="minimal", maxdepth=-1
        ):
        self.jackpath = jackpath
        self.verbosity = verbosity
        self.maxdepth = maxdepth

    @property
    def jackpath(self):
        """Path to .jack file"""
        return self._jackpath

    @jackpath.setter
    def jackpath(self, path):
        self._jackpath = path

    @property
    def verbosity(self):
        """Verbosity of output"""
        return self._verbosity

    @verbosity.setter
    def verbosity(self, opt):
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
        """Runs the compiler"""
        outdic = self._create_def_outdic()
        print_yellow("Starting translation of %s" % self.jackpath)
        contents = self._read_file()
        print(contents)
