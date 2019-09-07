#pylint: disable=missing-docstring

import os

from jackcompiler.utilities import list_files_with_ext, remove_comments

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

def generic_remove_comment(orig, rem, breaks):
    """Template function for testing comment removal"""
    rem_got = remove_comments(orig, breaks)
    assert rem == rem_got

def test_remove_comments():
    """Tests comment removal"""
    short_comment = "// Short comment\nnot a comment"
    generic_remove_comment(short_comment, "not a comment", [["//", "\n"]])
    long_comment = "/* long\ncomment\nhere */\nnot a comment"
    generic_remove_comment(long_comment, "not a comment", [["/*", "*/\n"]])
    long_comment_2 = "/** long\ncomment\nhere */\nnot a comment"
    generic_remove_comment(long_comment_2, "not a comment", [["/**", "*/\n"]])
