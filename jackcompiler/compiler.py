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

    def set_jackpath(self, path):
        """Sets the path to the jack file"""
        self._jackpath = path

    def get_jackpath(self):
        """Returns the path to the jack file"""
        return self._jackpath

    jackpath = property(get_jackpath, set_jackpath)

    def set_verbosity(self, opt):
        """Sets the verbosity option"""
        self._verbosity = opt

    def get_verbosity(self):
        """Returns the verbosity option"""
        return self._verbosity

    verbosity = property(get_verbosity, set_verbosity)

    def set_maxdepth(self, opt):
        """Sets the maxdepth option"""
        self._maxdepth = opt

    def get_maxdepth(self):
        """Returns the maxdepth option"""
        return self._verbosity

    maxdepth = property(get_maxdepth, set_maxdepth)

    def _create_def_outdic(self):
        """Creates the dictionary of output files"""
        outdic = {}
        outdic["tokens"] = self.jackpath.replace(".jack", "") + "T.xml"
        outdic["main"] = self.jackpath.replace(".jack", ".xml")
        return outdic

    def run(self):
        """Runs the compiler"""
        outdic = self._create_def_outdic()
        print_yellow("Starting translation of %s" % self.jackpath)
