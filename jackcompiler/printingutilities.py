"""Printing utility functions
"""

def print_dotted_line(width=80):
    """Prints a dotted line of the specified width"""
    print("-" * width)

def print_padded(string):
    """Prints message padded with dotted lines"""
    print_dotted_line()
    print(string)
    print_dotted_line()
