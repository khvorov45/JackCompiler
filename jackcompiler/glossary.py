"""Glossary
"""

KEYWORDS = [
    "class",
    "constructor", "function", "method",
    "field", "static", "var",
    "int", "char", "boolean", "void",
    "true", "false",
    "null",
    "this",
    "let", "do", 
    "if", "else",
    "while",
    "return"
]

SYMBOLS = [
    "{", "}",
    "(", ")",
    "[", "]",
    ".", ",", ";",
    "+", "-", "*", "/",
    "&", "|",
    "<", ">",
    "=",
    "~"
]

SYMBOL_ALIASES = {"<": "&lt;", "&": "&amp;", ">": "&gt;", '"': "&quot;"}
KEYWORD_CONSTANTS = {
    "true" : "push constant 0\nnot\n",
    "false" : "push constant 0\n",
    "null": "push constant 0\n",
    "this": "push pointer 0\n"
}
UNARY_OP = {"-": "neg\n", "~": "not\n"}
OPER = {
    "+": "add\n", "-" : "sub\n",
    "*": "call Math.multiply 2\n", "/": "call Math.divide 2\n",
    "&amp;": "and\n", "|": "or\n", "&lt;": "lt\n", "&gt;": "gt\n", "=": "eq\n"
}
SEGMENT = {
    "var": "local", "arg": "argument", "static": "static", "field": "this"
}

def is_op(tok):
    """Determines if the token is a an operator"""
    if tok["value"] in OPER.keys():
        return True
    return False

def is_term(tok):
    """Determines if the token represents a term"""
    if tok["value"] in KEYWORD_CONSTANTS.keys():
        return True
    some_term_types = ["integerConstant", "stringConstant", "identifier"]
    if tok["type"] in some_term_types:
        return True
    if tok["value"] == "(":
        return True
    if tok["value"] in UNARY_OP.keys():
        return True
    return False
