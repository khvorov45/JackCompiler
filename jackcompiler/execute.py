"""Functions related to executing the compilation from the command line"""

from cmdparserkhv import CmdParser, Cmdent

from .utilities import list_files_with_ext
from .compiler import JackCompiler

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
        "-v": Cmdent("verbosity"), # leave to JackCompiler to check correctness
        "-d": Cmdent("maxdepth", range(-1, 10^6)),
        "-tok": Cmdent("outtokens", "bool")
    }

    cmd = CmdParser(system_arguments, opt_dic)
    opts = cmd.get_all_options()
    paths = cmd.get_unrecognised()

    paths = list_files_with_ext(
        *paths, ext=".jack", maxdepth=opts["maxdepth"]
    )

    # Compile each of the found files
    comp = JackCompiler()
    comp.verbosity = opts["verbosity"]
    comp.outtokens = opts["outtokens"]
    for path in paths:
        comp.jackpath = path
        comp.run()
