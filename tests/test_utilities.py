#pylint: disable=missing-docstring

import os

from jackcompiler.utilities import list_files_with_ext

def test_list_files_with_ext():
    """Tests the function that lists files with particular extensions"""
    this_dir_path = os.path.dirname(os.path.realpath(__file__))
    file1dir = os.path.join(this_dir_path, "test_dir1")
    file2dir = os.path.join(file1dir, "test_dir2")
    all_files_expected = [
        os.path.join(file1dir, "test_file1.jack"),
        os.path.join(file2dir, "test_file2.jack")
    ]
    all_files_got = list_files_with_ext(file1dir, ext=".jack")
    assert all_files_expected == all_files_got
    one_file_expected = [all_files_expected[0]]
    one_file_got = list_files_with_ext(file1dir, ext=".jack", maxdepth=0)
    assert one_file_expected == one_file_got
