"""A collection of functions that run the translation
"""

from .printingutilities import print_padded
from .glossary import get_comment_breaks, get_verbosity_indicators
from .utilities import build_terminal
from .compilationengine import CompilationEngine
from .tokeniser import Tokeniser

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

def write_tokens(token_list, file_path):
    """Writes the token list to the specified file"""

    with open(file_path, "w+") as file_opened:

        file_opened.write("<tokens>\n")

        for tok in token_list:
            file_opened.write(build_terminal(tok))

        file_opened.write("</tokens>\n")

def run_translation(lexicon, jack_files, verbosity):
    """Controls compilation

    Arguments:
        lexicon: a dictionary with keywords and symbols
        jack_files: a list with filepaths to the .jack files to be compiled
        verbosity: verbosity of output. "full" or "minimal".
    """

    comment_breaks = get_comment_breaks()

    for jack_file in jack_files:

        out_tokens = jack_file.replace(".jack", "")
        out_tokens = out_tokens + "T.xml"
        out_main = jack_file.replace(".jack", ".xml")

        print_padded("Starting translation of %s" % jack_file)

        with open(jack_file) as jackfile:
            contents = jackfile.read()

        contents = remove_comments(contents, comment_breaks)

        contents_tokenised = Tokeniser(contents, lexicon).tokens

        if verbosity == get_verbosity_indicators()[0]:
            for tok in contents_tokenised:
                tok.print_message()

        write_tokens(contents_tokenised, out_tokens)

        # This should be where the input is compiled
        CompilationEngine(contents_tokenised, out_main)

        print_padded(
            "Wrote token list to %s \n And main to %s" % (out_tokens, out_main)
        )
