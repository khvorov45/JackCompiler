"""Functions related to executing the compilation from the command line"""

from cmdparserkhv import CmdParser, Cmdent

from .utilities import list_files_with_ext
from .compiler import JackCompiler
from .glossary import JACK_EXT, VERBOSITY_CHOICES

def run_cmd(system_arguments):
    """Runs the compiler given system arguments.

    Expected structure:
        path/to/script.py jackpaths [options]

    jackpaths is a list of .jack files or directories with .jack files
        (any order will do)

    Options:
        -v: verbosity indicator.
        -d: maximum recursion depth for traversing the directory.
    """

    opt_dic = {
        "-v": Cmdent("verbosity", VERBOSITY_CHOICES),
        "-d": Cmdent("maxdepth", range(-1, 10^6))
    }

    cmd = CmdParser(system_arguments, opt_dic)
    opts = cmd.get_all_options()
    paths = cmd.get_unrecognised()

    print(paths)
    print(opts)

    paths = list_files_with_ext(
        *paths, ext=JACK_EXT, maxdepth=opt_dic["maxdepth"]
    )

    # Compile each of the found files
    for path in paths:
        comp = JackCompiler(path, opts["verbosity"])
        comp.run()
