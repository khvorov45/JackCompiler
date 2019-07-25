"""Functions related to executing the compilation from the command line"""

import os

from .utilities import print_yellow, qte
from .compiler import JackCompiler

def run_cmd(system_arguments):
    """Runs the compiler given system arguments.

    Expected structure:
        path/to/script.py jackpath [options]

    jackpath is  a .jack file or directory with .jack files

    Options:
        -v: verbosity indicator.
        -d: maximum recursion depth for traversing the directory.
    """
    compiler_arguments = build_compiler_arguments(system_arguments)
    print(compiler_arguments)
    comp = JackCompiler(**compiler_arguments)
    comp.run()

def build_compiler_arguments(args):
    """Builds a dictionary of keyword arguments for the compiler
    given command-line input.
    """

    # Argument dictionary template
    comparg = {"filepath": "", "dirpath": ""}

    # Work out the file/directory argument
    try:
        jackfiles_path = args[1]
    except IndexError:
        raise Exception("Usage: jackcompiler.run path/to/file verbosity*")
    if os.path.isfile(jackfiles_path):
        comparg["filepath"] = jackfiles_path
    elif os.path.isdir(jackfiles_path):
        comparg["dirpath"] = jackfiles_path
    else:
        raise Exception(
            qte(jackfiles_path) + " is neither a file nor a directory"
        )

    # Work out the options
    comparg.update(get_cmd_options(args))

    return comparg

def get_cmd_options(args):
    """Returns a dictionary with all the optional arguments"""

    # Options indicators
    opt_ind = {
        "-v": build_option_entry("verbosity", get_verbosity),
        "-d": build_option_entry("maxdepth", get_maxdepth)
    }

    opts = {}

    # See what arguments have been provided
    for i, arg in enumerate(args):
        if arg in opt_ind.keys():
            candidate = opt_ind[arg]["fun"](args[i + 1])
            if candidate is not None:
                opts[opt_ind[arg]["name"]] = candidate

    return opts

def build_option_entry(name, fun):
    """Builds a dictionary entry for the options function"""
    return {"name": name, "fun": fun}

def get_verbosity(arg):
    """Returns the verbosity argument"""
    verbosity_choices = ["minimal", "full"]
    if arg not in verbosity_choices:
        print_yellow(
            "Verbosity indicator " + qte(arg) + " unrecognised. " + \
            "Using the default value."
        )
        return None
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
        return None
    return arg
