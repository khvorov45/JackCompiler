#pylint: disable=missing-docstring

import os
import re
from jackcompiler.compiler import JackCompiler
from jackcompiler.utilities import list_files_with_ext, COLOR
from jackcompiler.command_line import run_cmd

def compare_files(outdic):
    """Compares files"""
    for out_name in outdic:
        file1 = outdic[out_name]
        if not os.path.isfile(file1):
            continue
        file2 = re.sub(r"\..{2,3}$", r"Compare\g<0>", file1)
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

def test_syntax():
    """Tests tokeniser"""
    this_dir = os.path.dirname(os.path.realpath(__file__))
    syntax_dir = os.path.join(this_dir, "syntax")
    jackpaths = list_files_with_ext(syntax_dir, ext=".jack")
    comp = JackCompiler()
    comp.outtokens = True
    comp.outtree = True
    comp.outvm = False
    for jackpath in jackpaths:
        comp.jackpath = jackpath
        comp.run()
        compare_files(comp.get_outdic())

def test_vm_generation():
    """Tests VM code generation"""
    this_dir = os.path.dirname(os.path.realpath(__file__))
    syntax_dir = os.path.join(this_dir, "vmcode")
    jackpaths = list_files_with_ext(syntax_dir, ext=".jack")
    comp = JackCompiler()
    comp.outtokens = False
    comp.outtree = False
    comp.outvm = True
    for jackpath in jackpaths:
        comp.jackpath = jackpath
        comp.run()
        compare_files(comp.get_outdic())

def test_cmd_usage():
    """Tests usage from command line"""
    run_cmd(["jackcompiler", "vmcode/Average"])
