"""Glossary functions. Return strings with defined meanings.
"""

JACK_EXT = ".jack"
OUT_EXT = ".xml"
SOURCE_FOLDER_NAME = "src"
LEXICON_FOLDER_NAME = "LexicalElements"
SYMBOL_ALIASES = {"<": "&lt;", "&": "&amp;", ">": "&gt;", '"': "&quot;"}
KEYWORD_CONSTANTS = {
    "true" : "push constant 0\nnot\n",
    "false" : "push constant 0\n",
    "null": "dontknow",
    "this": "dontknow"
}
UNARY_OP = ["-", "~"]
OPER = {
    "+": "add\n", "-" : "sub\n",
    "*": "call Math.multiply 2\n", "/": "Math.divide 2\n",
    "&": "and\n", "|": "or\n", "<": "lt\n", ">": "gt\n", "=": "eq\n"
}
SEGMENT = {
    "var": "local", "arg": "argument", "static": "static", "field": "?field?"
}

def is_op(tok):
    """Determines if the token is a an operator"""
    if tok.token in OPER.keys():
        return True
    return False

def is_term(tok):
    """Determines if the token represents a term"""
    if tok.token in KEYWORD_CONSTANTS.keys():
        return True
    some_term_types = ["integerConstant", "stringConstant", "identifier"]
    if tok.toktype in some_term_types:
        return True
    if tok.token == "(":
        return True
    if tok.token in UNARY_OP:
        return True
    return False

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
