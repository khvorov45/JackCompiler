"""Glossary functions. Return strings with defined meanings.
"""

JACK_EXT = ".jack"
OUT_EXT = ".xml"
SOURCE_FOLDER_NAME = "src"
LEXICON_FOLDER_NAME = "LexicalElements"

def get_comment_breaks():
    """A list of comment breaks in form of [opener, closer]"""
    return [["//", "\n"], ["/**", "*/"], ["/*", "*/"]]

def get_verbosity_indicators():
    """Vebosity indicators. The first one is the default."""
    return ["full", "minimal"]

def get_print_indicator():
    """Print indicator"""
    return "print"

def get_empty_indicator():
    """Empty indicator"""
    return "null"
