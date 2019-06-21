"""Compare output.
Expected to be run form the command line with one argument - the directory with
.jack files to find.
"""

import sys
import os
import colorama

from src.utilities import list_files_with_ext
from src.glossary import JACK_EXT, OUT_EXT

colorama.init(autoreset=True)

def check_existence(file_path, filename):
    """Checks if a file exists"""

    file_exists = os.path.isfile(file_path)

    if file_exists:
        print(
            colorama.Fore.GREEN + "Found " +
            colorama.Fore.RESET + filename + " file " + file_path
        )
    else:
        print(
            colorama.Fore.RED + "Did not find " +
            colorama.Fore.RESET + filename + " file " + file_path
        )

    return file_exists

def compare_2(file1, filename1, file2, filename2):
    """Compares 2 files"""

    fail_msg = colorama.Fore.YELLOW + "Not comparing " + \
        filename1 + " to " + filename2
    result = True

    if not check_existence(file1, filename1):
        print(fail_msg)
        return None

    if not check_existence(file2, filename2):
        print(fail_msg)
        return None

    print(colorama.Fore.YELLOW + "Comparing " + filename1 + " to " + filename2)

    f1open = open(file1, "r")
    f2open = open(file2, "r")

    for f1line, f2line in zip(f1open, f2open):
        if f1line != f2line:
            result = False
            separator = colorama.Fore.RED + " | " + colorama.Fore.RESET
            msg = "{:_^10}" + separator + "{:_^10}"
            print(msg.format(f1line.strip(), f2line.strip()))

    f1open.close()
    f2open.close()

    if not result:
        print(colorama.Fore.RED + "Comparison failed")
    else:
        print(colorama.Fore.GREEN + "Comparison succeded")

    return result

def compare_files(directory):
    """Compares all files in a directory"""

    all_jack_files = list_files_with_ext(directory, JACK_EXT)

    tok_comps = []
    main_comps = []

    for jack_file in all_jack_files:

        print(
            colorama.Fore.YELLOW + "Looking at " +
            colorama.Fore.RESET + jack_file
        )

        xml_compare_file = jack_file.replace(JACK_EXT, "")

        xml_token_file = xml_compare_file + "T" + OUT_EXT
        xml_main_file = xml_compare_file + OUT_EXT

        xml_compare_file_token = xml_compare_file + "TCompare" + OUT_EXT
        xml_compare_file_main = xml_compare_file + "Compare" + OUT_EXT

        tok_comp = compare_2(
            xml_token_file, "token", xml_compare_file_token, "compare"
        )
        main_comp = compare_2(
            xml_main_file, "main", xml_compare_file_main, "compare"
        )

        tok_comps.append(tok_comp)
        main_comps.append(main_comp)

        print("")

    if any([not el and el is not None for el in tok_comps]):
        print(colorama.Fore.RED + "Some token comparisons failed")
    else:
        print(colorama.Fore.GREEN + "None of the token comparisons failed")
    if any([not el and el is not None for el in main_comps]):
        print(colorama.Fore.RED + "Some main comparisons failed")
    else:
        print(colorama.Fore.GREEN + "None of the main comparisons failed")

if __name__ == "__main__":
    compare_files(sys.argv[1])
