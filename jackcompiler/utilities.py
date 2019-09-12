"""General utility functions
"""

import os
import colorama

colorama.init(autoreset=True)

COLOR = {
    "red": colorama.Fore.RED,
    "green": colorama.Fore.GREEN,
    "yellow": colorama.Fore.YELLOW
}

def list_files_with_ext(*paths, ext, maxdepth=-1):
    """Creates a list of files with the specified extention"""
    needed_files = []
    for path in paths:
        if ext in path:
            needed_files.append(path)
            continue
        if not os.path.isdir(path):
            print_red(
                qte(path) + " is not a directory nor does it contain " +
                qte(ext) + ". Skipping."
            )
            continue
        path = os.path.realpath(path)
        start_level = path.count(os.sep)
        # pylint: disable=unused-variable
        # Need dirs to iterate
        for root, dirs, files in os.walk(path):
            depth = root.count(os.sep) - start_level
            if depth > maxdepth and (maxdepth != -1):
                break
            for filename in files:
                if ext in filename:
                    needed_files.append(os.path.join(root, filename))
    return needed_files

def remove_comments(file_contents, comment_breaks):
    """Removes all of the comments from a string"""
    for com_set in comment_breaks:
        opener = com_set[0]
        closer = com_set[1]
        while opener in file_contents:
            ind_start = file_contents.index(opener)
            keep_left = file_contents[:ind_start]
            rest = file_contents[ind_start:]
            keep_right = rest[rest.index(closer) + len(closer) : ]
            file_contents = keep_left + keep_right
    return file_contents

def print_yellow(lne):
    """Prints the given string in yellow"""
    print(colorama.Fore.YELLOW + lne)

def print_red(lne):
    """Prints the given string in red"""
    print(colorama.Fore.RED + lne)

def print_green(lne):
    """Prints the given string in green"""
    print(colorama.Fore.GREEN + lne)

def build_terminal(tok):
    """Builds a terminal statement for xml output"""
    terminal = "<" + tok["type"] + ">" + " " + \
        str(tok["value"]) + " " + "</" + tok["type"] + ">\n"
    return terminal

def qte(lne):
    """Quotes the given string"""
    return "'" + lne + "'"
