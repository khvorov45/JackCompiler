"""A collection of functions that run the translation
"""

from .printingutilities import print_padded
from .glossary import get_comment_breaks, get_verbosity_indicators
from .tokeninfo import TokenInfo

TAB_CHAR = "  "

def unexpected_token(tok):
    """Raises the unexpected token exception"""
    raise Exception("unexpected token: " + tok.token)

def compile_parameter_list(toks, ind, result, tab_level=1):
    """Compiles a parameter list (possibly empty)"""

    # First is the opening
    result += tab_level * TAB_CHAR + build_terminal(toks[ind])

    # Then come the parameters
    result += tab_level * TAB_CHAR + "<parameterList>\n"
    cur_ind = ind + 1
    while True:
        if toks[cur_ind].token == ")":
            break
        result += tab_level * TAB_CHAR + build_terminal(toks[cur_ind])
        cur_ind += 1
    result += tab_level * TAB_CHAR + "</parameterList>\n"

    # Finishes with closing the list
    result += tab_level * TAB_CHAR + build_terminal(toks[cur_ind])

    return [result, cur_ind + 1]

def compile_subroutine(toks, ind, result):
    """Compiles a subroutine"""

    # First is the opening
    result += TAB_CHAR + build_terminal(toks[ind])

    # Then is the subroutine type
    if toks[ind + 1].token not in ["constructor", "function", "method"]:
        unexpected_token(toks[ind])
    result += TAB_CHAR + "<subroutineDec>\n"
    result += 2 * TAB_CHAR + build_terminal(toks[ind + 1])

    # Next is the return type
    result += 2 * TAB_CHAR + build_terminal(toks[ind + 2])

    # Then is the name
    result += 2 * TAB_CHAR + build_terminal(toks[ind + 3])

    # Then is the parameter list
    par_list_comp = compile_parameter_list(toks, ind + 4, result, 2)
    result = par_list_comp[0]
    cur_ind = par_list_comp[1]

    # Then is the subroutine body
    result += 2 * TAB_CHAR + "<subroutineBody>\n"

    # First is the opening
    result += 3 * TAB_CHAR + build_terminal(toks[cur_ind])

    result += 2 * TAB_CHAR + "</subroutineBody>\n"

    result += TAB_CHAR + "</subroutineDec>\n"
    return result

def compile_class(toks, out_file_path):
    """Compiles an entire class"""

    # First token is 'class'
    if toks[0].token != "class":
        unexpected_token(toks[0])
    result = "<class>\n"
    result += TAB_CHAR + build_terminal(toks[0])

    # Second token is the class name
    if toks[1].toktype != "identifier":
        unexpected_token(toks[1])
    result += TAB_CHAR + build_terminal(toks[1])

    # Then is the class body
    result = compile_subroutine(toks, 2, result)

    result += "</class>\n"
    # Write to translation file
    out_file = open(out_file_path, "w+")
    out_file.write(result)
    out_file.close()

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

def build_terminal(tok):
    """Builds a terminal statement"""

    terminal = "<" + tok.toktype + ">" + " " + \
        str(tok.tokval) + " " + "</" + tok.toktype + ">\n"

    return terminal

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

        contents = add_whitespaces(contents, lexicon["symbols"])

        contents = contents.split()

        contents = unify_strings(contents)

        # This is where the input is tokenised
        contents = [TokenInfo(token, lexicon) for token in contents]

        if verbosity == get_verbosity_indicators()[0]:
            for tok in contents:
                tok.print_message()

        write_tokens(contents, out_tokens)

        # This should be where the input is compiled
        compile_class(contents, out_main)

        print_padded(
            "Wrote token list to %s \n And main to %s" % (out_tokens, out_main)
        )
