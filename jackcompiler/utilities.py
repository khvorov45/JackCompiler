"""General utility functions
"""

import os

from .glossary import LEXICON_FOLDER_NAME, JACK_EXT, VERBOSITY

def run(args):
    """Runs the compiler
    Is meant to accept command line arguments:
        directory with .jack files
        verbosity of output ('full' or 'minimal')
    All of the .jack files will be compiled and saved in the same direcotry with
    the same names but different extensions.
    """
    try:
        jackfiles = get_jack_files(args[1])
    except IndexError:
        print("Usage: jackcompiler.run path/to/file verbosity*")
        return
    if not jackfiles:
        return
    try:
        verbosity = get_verbosity(args[2])
    except IndexError:
        verbosity = VERBOSITY[0]

    lexicon = load_folder(get_src_path(LEXICON_FOLDER_NAME))

    run_translation(lexicon, jackfiles, verbosity)

def get_jack_files(jackname):
    """Returns the list of all the .jack file paths"""
    jackfiles = []
    if os.path.isfile(jackname):
        jackfiles = jackname
        if JACK_EXT not in jackname:
            print(jackname + " is not a .jack file")
        return jackfiles
    if os.path.isdir(jackname):
        jackfiles = list_files_with_ext(jackname, JACK_EXT)
        if not jackfiles:
            print(jackname + " has no .jack files in it")
        return jackfiles
    print(jackname + " is not a file or a directory")
    return jackfiles

def load_folder(folder_path):
    """Loads all text (.txt) files in a folder as a dictionary"""
    all_files = os.listdir(folder_path)
    contents = {}
    for one_file in all_files:
        if ".txt" not in one_file:
            continue
        one_file_path = os.path.join(folder_path, one_file)
        with open(one_file_path) as one_file_opened:
            lns = one_file_opened.readlines()
        lns = [el.strip() for el in lns]
        contents[one_file.replace(".txt", "")] = lns
    return contents

def get_src_path(entity_name):
    """Returns the path to the named entity in the source folder"""
    src_path = os.path.dirname(os.path.realpath(__file__))
    src_path = os.path.join(src_path, entity_name)
    return src_path

def list_files_with_ext(dirname, ext):
    """Creates a list of files with the specified extention"""

    dirname = os.path.realpath(dirname)

    jack_files = []
    # pylint: disable=unused-variable
    # dirs needs to be there in order to be able to iterate
    for root, dirs, files in os.walk(dirname):
        for filename in files:
            if ext in filename:
                jack_files.append(os.path.join(dirname, root, filename))

    return jack_files

def get_verbosity(verbosity_ind):
    """Returns the verbosity argument. Default is full."""
    if verbosity_ind not in VERBOSITY:
        print(verbosity_ind + " unrecognised, defaulting to " + VERBOSITY[0])
        return VERBOSITY[0]
    return verbosity_ind

def count_kind(lis, knd):
    """Counts elements of the given kind"""
    cnt = 0
    for ent in lis:
        if ent.kind == knd:
            cnt += 1
    return cnt

def build_terminal(tok):
    """Builds a terminal statement for xml output"""

    terminal = "<" + tok.toktype + ">" + " " + \
        str(tok.tokval) + " " + "</" + tok.toktype + ">\n"

    return terminal

class UnexpectedToken(Exception):
    """Exception raised for unexpected tokens in input"""
    def __init__(self, tok):
        super().__init__("unexpected token: " + tok.token)
