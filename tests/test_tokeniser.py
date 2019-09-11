#pylint: disable=missing-docstring

import os
from jackcompiler.compiler import JackCompiler
from jackcompiler.utilities import list_files_with_ext, COLOR

def compare_files(file1, file2):
    """Compares files"""
    result = True
    f1open = open(file1, "r")
    f2open = open(file2, "r")
    for f1line, f2line in zip(f1open, f2open):
        if f1line.strip() != f2line.strip():
            result = False
            separator = COLOR["red"] + " | "
            msg = "{:_^10}" + separator + "{:_^10}"
            print(msg.format(f1line.strip(), f2line.strip()))
    f1open.close()
    f2open.close()
    assert result

def test_tokeniser():
    """Tests tokeniser"""
    this_dir = os.path.dirname(os.path.realpath(__file__))
    syntax_dir = os.path.join(this_dir, "syntax")
    jackpaths = list_files_with_ext(syntax_dir, ext=".jack")
    comp = JackCompiler()
    comp.outtokens = True
    for jackpath in jackpaths:
        comp.jackpath = jackpath
        comp.run()
        tokfile = comp.get_outdic()["tokens"]
        tokfile_compare = tokfile.replace(".xml", "Compare.xml")
        compare_files(tokfile, tokfile_compare)
