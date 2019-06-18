"""Compare output
"""

import sys
import os

from src.utilities import list_files_with_ext
from src.glossary import JACK_EXT, OUT_EXT

def compare_files(directory):
    """Compares two files"""
    all_jack_files = list_files_with_ext(directory, JACK_EXT)
    for jack_file in all_jack_files:

        print("Looking at " + jack_file)

        xml_token_file = jack_file.replace(JACK_EXT, "")
        xml_token_file = xml_token_file + "T" + OUT_EXT
        xml_out_file = jack_file.replace(JACK_EXT, OUT_EXT)
        xml_compare_file = jack_file.replace(JACK_EXT, "")
        xml_compare_file_main = xml_compare_file + "Compare" + OUT_EXT
        xml_compare_file_token = xml_compare_file + "TCompare" + OUT_EXT

        if os.path.isfile(xml_token_file) and \
        os.path.isfile(xml_compare_file_token):
            print("Found token file " + xml_token_file)
            print("Found comparison file " + xml_compare_file_token)
            toks = open(xml_token_file, "r")
            comp = open(xml_compare_file_token, "r")

            for my_line, comp_line in zip(toks, comp):

                if my_line != comp_line:
                    print("MY:  " + my_line + "COMP:" + comp_line + "\n")

            toks.close()
            comp.close()
        else:
            print("Did not find token file " + xml_token_file)

        if os.path.isfile(xml_out_file):
            print("Found out file " + xml_out_file)
        else:
            print("Did not find out file " + xml_out_file)

        print("")

if __name__ == "__main__":
    compare_files(sys.argv[1])
