"""General utility functions
"""

import os

def list_files_with_ext(jackdir, ext):
    """Creates a list of files with the specified extention"""

    jackdir = os.path.realpath(jackdir)

    # Only one .jack file
    if ext in jackdir:
        return [jackdir]

    # Get .jack files in the directory
    jack_files = []
    # pylint: disable=unused-variable
    # dirs needs to be there in order to be able to iterate
    for root, dirs, files in os.walk(jackdir):
        for filename in files:
            if ext in filename:
                jack_files.append(os.path.join(jackdir, root, filename))

    return jack_files
