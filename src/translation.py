"""A collection of functions that run the translation
"""

from .printingutilities import print_padded
from .glossary import get_comment_breaks, get_verbosity_indicators
from .tokeninfo import TokenInfo

def remove_comments(file_contents, comment_breaks):
    """Removes all of the comments from a string"""

    for com_set in comment_breaks:
        opener = com_set[0]
        closer = com_set[1]

        while opener in file_contents:
            ind_start = file_contents.index(opener)

            keep_left = file_contents[:ind_start]
            rest = file_contents[ind_start:]
            if closer == "\n":
                keep_right = rest[rest.index(closer) : ]
            else: keep_right = rest[rest.index(closer) + len(closer) : ]
            file_contents = keep_left + keep_right

    return file_contents

def add_whitespaces(file_contents, symbols):
    """Adds whitespaces around symbols"""
    for symbol in symbols:
        if symbol in file_contents:
            file_contents = file_contents.replace(symbol, " " + symbol + " ")
    return file_contents

def unify_strings(token_list):
    """Unify string literals into a single token"""

    tokens_new = []
    inside_string = False
    for token in token_list:

        # Single-word string
        if token.count('"') == 2:
            tokens_new.append(token)
            continue

        # Multi-word string
        if inside_string:
            tokens_new[-1] += " " + token
        else:
            tokens_new.append(token)

        if '"' in token:
            inside_string = not inside_string

    return tokens_new

def run_translation(lexicon, jack_files, verbosity):
    """Controls compilation

    Arguments:
        lexicon: a dictionary with keywords and symbols
        jack_files: a list with filepaths to the .jack files to be compiled
        verbosity: verbosity of output. "full" or "minimal".
    """

    comment_breaks = get_comment_breaks()

    for jack_file in jack_files:

        out_path = jack_file.replace(".jack", ".xml")

        print_padded("Starting translation of %s" % jack_file)

        with open(jack_file) as jackfile:
            contents = jackfile.read()

        contents = remove_comments(contents, comment_breaks)

        contents = add_whitespaces(contents, lexicon["symbols"])

        contents = contents.split()

        contents = unify_strings(contents)

        contents = [TokenInfo(token, lexicon) for token in contents]

        if verbosity == get_verbosity_indicators()[0]:
            for tok in contents:
                tok.print_message()

        print_padded("Wrote translation to %s" % out_path)
