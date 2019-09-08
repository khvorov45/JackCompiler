#pylint: disable=missing-docstring

import os
from jackcompiler.tokeniser import Tokeniser

def test_tokeniser():
    """Tests tokeniser"""
    this_dir = os.path.dirname(os.path.realpath(__file__))
    syntax_dir = os.path.join(this_dir, "syntax")
