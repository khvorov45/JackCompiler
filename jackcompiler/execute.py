"""Functions related to executing the compilation from the command line"""

from cmdparserkhv import CmdParser

from .utilities import list_files_with_ext, pull_option, print_yellow, qte
from .compiler import JackCompiler
from .glossary import JACK_EXT, DEF_MAX_DEPTH, DEF_VERBOSITY, VERBOSITY_CHOICES

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

    # Options
    opt_inds = {
        "-v": ["verbosity", get_verbosity],
        "-d": ["max_depth", get_maxdepth]
    }

    cmd = CmdParser(system_arguments, opt_inds)
    opts = cmd.get_opts()
    paths = cmd.get_unproc()

    print(opts)
    print(paths)

    raise Exception()

    # Find all the .jack files
    maxdepth = pull_option(opts, "maxdepth", DEF_MAX_DEPTH)
    paths = list_files_with_ext(
        *paths, ext=JACK_EXT, maxdepth=maxdepth
    )

    # Compile each of the found files
    verbosity = pull_option(opts, "verbosity", DEF_VERBOSITY)
    for path in paths:
        comp = JackCompiler(path, verbosity)
        comp.run()

def get_verbosity(arg):
    """Returns the verbosity argument"""
    if arg not in VERBOSITY_CHOICES:
        print_yellow(
            "Verbosity indicator " + qte(arg) + " unrecognised. " + \
            "Using the default value."
        )
        return DEF_VERBOSITY
    return arg

def get_maxdepth(arg):
    """Returns the maxdepth argument"""
    try:
        arg = int(arg)
    except ValueError:
        print_yellow(
            "Maximum depth value " + qte(arg) + " is not an integer. " + \
            "Using the default value."
        )
        return DEF_MAX_DEPTH
    return arg
