"""Functions related to executing the compilation from the command line"""

import sys
from cmdparserkhv import CmdParser, Cmdent

from .utilities import list_files_with_ext
from .compiler import JackCompiler

def main():
    """Runs when called as execultable"""
    run_cmd(sys.argv)

def run_cmd(system_arguments):
    """Runs from the command line.

    Expected structure:
        path/to/script.py jackpaths [options]

    jackpaths is a list of .jack files or directories with .jack files
        (any order will do)

    Options:
        -v: verbosity indicator. "full" or "minimal"
        -d: maximum recursion depth for traversing the directory.
        -tok: Output tokens
        -tree: Output xml tree
        -novm: Do not output vm code
        -h: Show help
    """

    opt_dic = {
        "-v": Cmdent("verbosity", ["minimal", "full"]),
        "-d": Cmdent("maxdepth", range(-1, 10^6)),
        "-tok": Cmdent("outtokens", "bool"),
        "-tree": Cmdent("outtree", "bool"),
        "-novm": Cmdent("novm", "bool"),
        "-h": Cmdent("help", "bool")
    }

    cmd = CmdParser(system_arguments, opt_dic)
    opts = cmd.get_all_options()
    paths = cmd.get_unrecognised()

    if opts["help"] or not paths:
        show_help()
        return

    paths = list_files_with_ext(
        *paths, ext=".jack", maxdepth=opts["maxdepth"]
    )

    # Compile each of the found files
    comp = JackCompiler()
    comp.verbosity = opts["verbosity"]
    comp.outtokens = opts["outtokens"]
    comp.outtree = opts["outtree"]
    comp.outvm = not opts["novm"]
    for path in paths:
        comp.jackpath = path
        comp.run()

def show_help():
    """Prints help"""
    print("\nUsage: jackcompiler [options] paths/to/jack\n")
    print_options()

def print_options():
    """Prints all the usage options"""
    print(
        """Options:\n
        -v: verbosity indicator. "full" or "minimal"\n
        -d: maximum recursion depth for traversing the directory.\n
        -tok: Output tokens\n
        -tree: Output xml tree\n
        -novm: Do not output vm code\n
        -h: Show this message\n"""
    )
