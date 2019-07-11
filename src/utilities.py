"""General utility functions
"""

import os

def find_segment(var_kind):
    """Returns the VM segment for the given kind"""
    if var_kind == "var":
        return "local"
    return "noidea"

def vmcom(com, seg, ind):
    """VM two-entry command like 'push local 1'"""
    return  com + " " + seg + " " + str(ind)

def count_kind(dic, knd):
    """Counts elements of the given kind"""
    cnt = 0
    for ent in dic.values():
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

def list_files_with_ext(jackdir, ext):
    """Creates a list of files with the specified extention"""

    jackdir = os.path.realpath(jackdir)

    # Only one .jack file
    if ext in jackdir:
        return [jackdir]

    # Get .jack files in the directory
    jack_files = []
    # pylint: disable=unused-variable
    # dirs needs to be there in order to be able to iterate
    for root, dirs, files in os.walk(jackdir):
        for filename in files:
            if ext in filename:
                jack_files.append(os.path.join(jackdir, root, filename))

    return jack_files
