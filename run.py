"""Example of a script that can be ran from command line to run
the Jack compiler

Command line arguments expected:
    directory with .jack files
    verbosity of output ('full' or 'minimal'). Optional.
        Will default to 'minimal'.

All of the .jack files will be compiled and saved in the same direcotry with
the same names but different extensions.
"""
import sys

import jackcompiler

if __name__ == "__main__":
    jackcompiler.run_cmd(sys.argv)
